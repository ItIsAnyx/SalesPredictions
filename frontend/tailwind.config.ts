import type { Config } from 'tailwindcss'

export default {
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        'secondary-fixed-dim': '#6bd8cb',
        'tertiary-container': '#001a42',
        'outline': '#76777d',
        'primary-container': '#131b2e',
        'secondary': '#006a61',
        'secondary-container': '#86f2e4',
        'primary': '#000000',
        'background': '#f8f9ff',
        'on-background': '#0b1c30',
        'surface': '#f8f9ff',
        'surface-container-low': '#eff4ff',
        'surface-container': '#e5eeff',
        'surface-container-highest': '#d3e4fe',
        'surface-variant': '#d3e4fe',
        'error': '#ba1a1a',
        'on-surface': '#0b1c30',
        'on-surface-variant': '#45464d',
        'outline-variant': '#c6c6cd'
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