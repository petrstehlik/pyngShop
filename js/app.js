app.config(function($routeProvider, $locationProvider){
	$locationProvider.html5Mode(true);

	$routeProvider
		.when('/login', {
			controller: 'loginController',
			templateUrl: SETTINGS.views() + 'login.html',
			// resolve: {
			// 	isLogin: checkLogin
			// }
		})
		.when('/', {
			controller: 'homeController',
			templateUrl: SETTINGS.views() + 'home.html',
			// resolve: {
			// 	isLogin: checkLogin
			// }
		})
		.when('/404', {
			controller: 'homeController',
			templateUrl: SETTINGS.views() + 'home.html',
			// resolve: {
			// 	isLogin: checkLogin
			// }
		})
		.otherwise({
			redirectTo: '/404'
		});
});