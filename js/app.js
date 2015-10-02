var app = angular.module('pyngShop', ['ngAnimate', 'ngMaterial', 'ngRoute' ]);

app.constant('SETTINGS', {
	template : 'default'
});

app.config(function($routeProvider, SETTINGS){

	console.log(SETTINGS.template);
	$routeProvider
		.when('/login', {
			controller: 'loginController',
			templateUrl: 'templates/' + SETTINGS.template  +'/login.html',
			// resolve: {
			// 	isLogin: checkLogin
			// }
		})
		.when('/', {
			controller: 'homeController',
			templateUrl: 'templates/' + SETTINGS.template  +'/home.html',
			// resolve: {
			// 	isLogin: checkLogin
			// }
		})
		.when('/404', {
			controller: 'homeController',
			templateUrl: 'templates/' + SETTINGS.template + '/home.html',
			// resolve: {
			// 	isLogin: checkLogin
			// }
		})
		.otherwise({
			redirectTo: '/404'
		});

});