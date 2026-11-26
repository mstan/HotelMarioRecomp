#pragma once
#include "recomp_launcher.h"
static int diagnostics_feature_count(void *ctx){(void)ctx;return 1;}
static int diagnostics_feature_get(void *ctx,int index,RecompLauncherCModFeature *out) {
    if(index)return 0;CdiPlayerConfig *config=ctx;memset(out,0,sizeof *out);
    strcpy(out->id,"input-recording");strcpy(out->package_id,"cdi.diagnostics");strcpy(out->package_version,"1.0.0");strcpy(out->package_name,"Gameplay Diagnostics");strcpy(out->name,"Gameplay Diagnostics");
    strcpy(out->description,"Record controller input and frame numbers for gameplay diagnostics. This choice is remembered independently of display settings.");
    strcpy(out->group,"Diagnostics");out->enabled=config->diagnostics_recording;return 1;
}
static int diagnostics_feature_enable(void *ctx,const char *package,const char *feature,int enabled) {
    if(strcmp(package,"cdi.diagnostics") || strcmp(feature,"input-recording"))return 0;
    ((CdiPlayerConfig*)ctx)->diagnostics_recording=!!enabled;return 1;
}
static int diagnostics_mod_commit(void *ctx,const char *image){(void)ctx;(void)image;return 1;}
