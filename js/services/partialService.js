app.directive("mainMenu", function() {
	return {
		scope: {
			section: '=',
		},
		templateUrl: SETTINGS.partials() + 'mainmenu.html'
	};
});

app.controller('mainMenuController', function($scope){
	$scope.menu = [
		{
			"title" : "Item #1",
			"href"	: "/login",
		},
		{
			"title" : "Item #2",
			"href"	: "/login",
		},
		{
			"title" : "Item #3",
			"href"	: "/login",
		}
	]
})