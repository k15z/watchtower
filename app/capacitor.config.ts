import { CapacitorConfig } from '@capacitor/cli';

const config: CapacitorConfig = {
  appId: 'dev.kevz.watchtower',
  appName: 'Watchtower',
  webDir: 'dist',
  server: {
    androidScheme: 'https'
  }
};

export default config;
