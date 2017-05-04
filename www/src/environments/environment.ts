// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `angular-cli.json`.

export const environment = {
  production: false,
  apiUrl : "/api",
  ftas : {
    /**
      * simple URL (without protocol) to FTAS instance
      */
    url : "ftas.cesnet.cz",
    /**
      * Full URL to filtering script (usually "example.com/ftas/stat.pl")
      * Specify URL without URL (https is forced)
      * If this option is not set, url must be.
      * If both are set, fullUrl is used.
      */
    fullUrl : undefined,
    /**
      * Specify which output machines will be used
      * Can be a list (as string): "1,2,5,10"
      */
    output : "1402"
  },
  nerd : {
    /**
      * simple URL (without protocol) to FTAS instance
      */
    url : "nerd.cesnet.cz/nerd",
    /**
      * Full URL to filtering script (usually "example.com/ftas/stat.pl")
      * Specify URL without URL (https is forced)
      * If this option is not set, url must be.
      * If both are set, fullUrl is used.
      */
    fullUrl : undefined,
  },
  securityCloud : {
    /**
      * simple URL (without protocol) to FTAS instance
      */
    url : undefined,
    /**
      * Full URL to filtering script (usually "example.com/ftas/stat.pl")
      * Specify URL without URL (https is forced)
      * If this option is not set, url must be.
      * If both are set, fullUrl is used.
      */
    fullUrl : "/scgui",
    /**
      * Set resolution of the graph output
      * Default: 2
      */
    resolution : 2
  }
};

// The list of which env maps to which file can be found in `angular-cli.json`.
