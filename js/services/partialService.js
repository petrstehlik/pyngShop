app.directive("mainMenu", function() {
	return {
		scope: {
			section: '='
		},
		templateUrl: SETTINGS.partials() + 'mainmenu.html'
	};
});