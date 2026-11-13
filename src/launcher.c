#include "cdi_launcher.h"
#include "recomp_launcher.h"
#include "launcher_profile.h"
#include "cdi_sha256.h"
#include "disc_parser.h"
#include "bios_identity.h"
#include "game_identity.h"
#include <SDL.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

static int verify_bios(const char *path, RecompLauncherCBiosVerify *out) {
    memset(out,0,sizeof *out);
    FILE *file=path && *path ? fopen(path,"rb") : NULL;
    if(!file) { snprintf(out->detail,sizeof out->detail,"Select your CD-i player BIOS.");return 1; }
    uint8_t *bytes=malloc(CDI_COMPILED_BIOS_SIZE+1u),digest[32];
    if(!bytes){fclose(file);return 0;}
    size_t size=fread(bytes,1,CDI_COMPILED_BIOS_SIZE+1u,file);
    int failed=ferror(file);fclose(file);
    if(!failed && size==CDI_COMPILED_BIOS_SIZE) {
        cdi_sha256(bytes,size,digest);
        out->ok=!memcmp(digest,cdi_compiled_bios_sha256,sizeof digest);
    }
    free(bytes);
    snprintf(out->detail,sizeof out->detail,out->ok ? "Matches this build's compiled BIOS." :
             "BIOS does not match this build. Rebuild with your supported BIOS.");
    return 1;
}

static void read_asset_sidecar(const char *name,char *path,size_t capacity) {
    if(*path)return;
    char filename[1024];
    char *base=SDL_GetBasePath();
    snprintf(filename,sizeof filename,"%s%s.cfg",base ? base : "",name);
    SDL_free(base);
    FILE *file=fopen(filename,"r");
    if(!file)return;
    if(fgets(path,(int)capacity,file))path[strcspn(path,"\r\n")]=0;
    fclose(file);
}

static int verify_disc(const char *path, RecompLauncherCDiscVerify *out) {
    memset(out,0,sizeof *out);
    CdiDisc disc;
    if(!cdi_disc_open(path,&disc)){out->verdict=3;return 1;}
    uint8_t digest[32];
    out->iso_ok=disc.track_mode==2 && disc.sector_count==156100 &&
        cdi_sha256_file(disc.bin_path,digest) && !memcmp(digest,hotelmario_disc_sha256,32);
    out->verdict=out->iso_ok ? 1 : 3;
    out->track_count=1;
    snprintf(out->region,sizeof out->region,"%s",HOTELMARIO_GAME_REGION);
    cdi_disc_close(&disc);
    return 1;
}

typedef struct {CdiPlayerConfig *config;const char *path;} SetupContext;
static int persist_setup(void *opaque,const char *disc,const char *bios) {
    SetupContext *context=opaque;
    if(strlen(disc)>=sizeof context->config->disc_path || strlen(bios)>=sizeof context->config->bios_path)return 1;
    strcpy(context->config->disc_path,disc);
    strcpy(context->config->bios_path,bios);
    return cdi_player_config_save(context->path,context->config) ? 0 : 1;
}

int cdi_launcher_run(const char *initial_bios,const char *initial_disc,
                     char *bios,size_t bios_capacity,char *disc,size_t disc_capacity,
                     CdiPlayerConfig *config,const char *config_path) {
    RecompLauncherCSettings settings={0};
    RecompLauncherCGameInfo game={0};
    if(!initial_bios)read_asset_sidecar("bios",config->bios_path,sizeof config->bios_path);
    if(!initial_disc)read_asset_sidecar("disc",config->disc_path,sizeof config->disc_path);
    launcher_profile_apply("cdi",&game);
    static const char *aspects[]={"Original 4:3","Fit to screen"};
    game.name=HOTELMARIO_GAME_NAME;game.region=HOTELMARIO_GAME_REGION;
    game.aspect_labels=aspects;game.num_aspect_labels=2;
    game.aspect_setting_help="Fit the original CD-i picture to the window. This does not expand the game's field of view.";
    game.has_window_size=1;
    game.config_path=config_path;
    game.disc_verify=verify_disc;game.bios_verify=verify_bios;
    game.rom_patterns=kCdiRomPatterns;game.num_rom_patterns=2;
    game.boxart_path="assets/img/hotel-mario-title.png";
    game.setup_wizard_supported=1;
    game.has_mouse_controls=1;
    SetupContext context={config,config_path};
    game.persist_setup=persist_setup;game.persist_setup_ctx=&context;
    settings.window_scale=2;
    settings.window_width=config->window_width;
    settings.aspect_index=config->fit_to_screen;
    settings.fullscreen=config->fullscreen;
    settings.linear_filter=config->linear_filter;
    settings.enable_audio=config->enable_audio;
    settings.audio_freq=44100;
    settings.volume=config->volume;
    settings.skip_launcher=config->skip_launcher;
    settings.player_src[0]=config->input_source;
    settings.mouse_enabled=config->enable_mouse;
    settings.mouse_sensitivity=config->mouse_sensitivity;
    settings.mouse_invert_x=config->mouse_invert_x;
    settings.mouse_invert_y=config->mouse_invert_y;
    memcpy(settings.mouse_bind,config->mouse_bind,sizeof config->mouse_bind);
    memcpy(settings.player_key_bind[0],config->key_bind,sizeof config->key_bind);
    memcpy(settings.player_pad_bind[0],config->pad_bind,sizeof config->pad_bind);
    snprintf(settings.player_gamepad_guid[0],sizeof settings.player_gamepad_guid[0],"%s",config->gamepad_guid);
    snprintf(settings.bios_path,sizeof settings.bios_path,"%s",initial_bios ? initial_bios : config->bios_path);
    const char *initial=initial_disc ? initial_disc : config->disc_path;
    char *base=SDL_GetBasePath();
    char assets[1024];
    snprintf(assets,sizeof assets,"%sassets",base ? base : "");
    SDL_free(base);
    recomp_launcher_set_preserve_sdl(1);
    int result=recomp_launcher_run_window(HOTELMARIO_GAME_NAME,&settings,&game,assets,initial,disc,disc_capacity);
    config->fit_to_screen=settings.aspect_index==1;
    config->window_width=settings.window_width;
    config->fullscreen=settings.fullscreen;
    config->linear_filter=settings.linear_filter;
    config->enable_audio=settings.enable_audio;
    config->volume=settings.volume;
    config->skip_launcher=settings.skip_launcher;
    config->input_source=settings.player_src[0];
    config->gamepad_instance=settings.player_gamepad_instance[0];
    config->enable_mouse=settings.mouse_enabled;
    config->mouse_sensitivity=settings.mouse_sensitivity;
    config->mouse_invert_x=settings.mouse_invert_x;
    config->mouse_invert_y=settings.mouse_invert_y;
    memcpy(config->mouse_bind,settings.mouse_bind,sizeof config->mouse_bind);
    memcpy(config->key_bind,settings.player_key_bind[0],sizeof config->key_bind);
    memcpy(config->pad_bind,settings.player_pad_bind[0],sizeof config->pad_bind);
    snprintf(config->gamepad_guid,sizeof config->gamepad_guid,"%s",settings.player_gamepad_guid[0]);
    snprintf(config->bios_path,sizeof config->bios_path,"%s",settings.bios_path);
    if(result==RECOMP_LAUNCHER_RESULT_LAUNCH)snprintf(config->disc_path,sizeof config->disc_path,"%s",disc);
    if(!cdi_player_config_save(config_path,config))return 2;
    if(result==RECOMP_LAUNCHER_RESULT_QUIT)return 1;
    if(result!=RECOMP_LAUNCHER_RESULT_LAUNCH)return 2;
    RecompLauncherCBiosVerify check;
    RecompLauncherCDiscVerify media;
    if(!verify_bios(settings.bios_path,&check) || !check.ok || !verify_disc(disc,&media) || media.verdict!=1)return 2;
    if(snprintf(bios,bios_capacity,"%s",settings.bios_path)>=(int)bios_capacity)return 2;
    return 0;
}
