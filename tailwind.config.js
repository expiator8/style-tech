module.exports = {
  purge: [],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily:{
        'title':['Roboto', '"Nanum Gothic"', 'Arial', 'verdana', 'sans-serif'],
        'u-title':['Roboto', '"Nanum Gothic"', 'Arial', 'verdana', 'sans-serif'],
      },
      fontSize:{
        'title':'32px',
        'u-title':'18px',
      },
      letterSpacing: {
        title: '.2em'
      },
      spacing:{
        '20':'200px',
        "75":'750px',
        '90':'900px',
        'pl':'133px',
        '46':'11.5rem',
        '88':'20.5rem',
        '97':'41.25rem',
        '1/5':'20%',
        'btn':'10.625rem',
      },
      backgroundColor: theme => ({
        'white2':'#FFFFFF',
      }),
    },
  },
  variants: {
    extend: {},
  },
  plugins: [],
}
