import {Config} from '@remotion/cli/config';

Config.setVideoImageFormat('jpeg');
Config.setOverwriteOutput(true);
Config.setPublicDir(process.env.TMF_PUBLIC_DIR || './public');
