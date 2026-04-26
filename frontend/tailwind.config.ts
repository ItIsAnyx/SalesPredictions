import type { Config } from 'tailwindcss'

export default {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        "secondary-fixed-dim": "#6bd8cb",
                        "tertiary-container": "#001a42",
                        "on-primary-fixed-variant": "#3f465c",
                        "outline": "#76777d",
                        "primary-container": "#131b2e",
                        "inverse-primary": "#bec6e0",
                        "on-error": "#ffffff",
                        "on-secondary": "#ffffff",
                        "surface-container": "#e5eeff",
                        "secondary": "#006a61",
                        "secondary-fixed": "#89f5e7",
                        "on-primary-container": "#7c839b",
                        "secondary-container": "#86f2e4",
                        "primary": "#000000",
                        "inverse-surface": "#213145",
                        "on-surface-variant": "#45464d",
                        "outline-variant": "#c6c6cd",
                        "background": "#f8f9ff",
                        "on-tertiary": "#ffffff",
                        "surface-dim": "#cbdbf5",
                        "surface-container-highest": "#d3e4fe",
                        "on-error-container": "#93000a",
                        "on-secondary-container": "#006f66",
                        "tertiary": "#000000",
                        "surface-bright": "#f8f9ff",
                        "tertiary-fixed-dim": "#adc6ff",
                        "on-primary": "#ffffff",
                        "on-secondary-fixed": "#00201d",
                        "on-background": "#0b1c30",
                        "surface": "#f8f9ff",
                        "surface-container-high": "#dce9ff",
                        "primary-fixed-dim": "#bec6e0",
                        "tertiary-fixed": "#d8e2ff",
                        "error-container": "#ffdad6",
                        "on-tertiary-fixed": "#001a42",
                        "surface-container-low": "#eff4ff",
                        "on-primary-fixed": "#131b2e",
                        "error": "#ba1a1a",
                        "on-surface": "#0b1c30",
                        "surface-tint": "#565e74",
                        "on-tertiary-container": "#3980f4",
                        "on-secondary-fixed-variant": "#005049",
                        "surface-container-lowest": "#ffffff",
                        "inverse-on-surface": "#eaf1ff",
                        "primary-fixed": "#dae2fd",
                        "surface-variant": "#d3e4fe",
                        "on-tertiary-fixed-variant": "#004395"
      },

      spacing: {
        xs: '4px',
        sm: '8px',
        md: '16px',
        lg: '24px',
        xl: '32px',
        'container-margin': '40px'
      },

      fontFamily: {
        manrope: ['Manrope'],
        inter: ['Inter']
      }
    }
  }
}