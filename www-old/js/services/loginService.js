app.service('theme', function() {
      var themePath = SETTINGS.templatePath();
      return {
        path : function() { console.log(themePath); return themePath; }
        //setTitle: function(newTitle) { title = newTitle; }
      };
    });