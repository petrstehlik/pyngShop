app.config(function($routeProvider, $locationProvider){

	$locationProvider.html5Mode(false);

	$routeProvider
		.when('/login', {
			controller: 'loginController',
			templateUrl: SETTINGS.views() + 'login.html',
			resolve: {
				isLoggedIn: checkLogin
			}
		})
		.when('/', {
			controller: 'homeController',
			templateUrl: SETTINGS.views() + 'home.html',
			resolve: {
				isLoggedIn: checkLogin
			}
		})
		.when('/cart', {
			controller: 'cartController',
			templateUrl: SETTINGS.views() + 'cart.html',
			resolve: {
				isLoggedIn: checkLogin,
				exists : checkPage
			}
		})
		.when('/:category', {
			controller: 'categoryController',
			templateUrl: SETTINGS.views() + 'category.html',
			resolve: {
				isLoggedIn: checkLogin,
				exists : checkPage
			}
		})
		.when('/:category*/p/:product', {
			controller: 'productController',
			templateUrl: SETTINGS.views() + 'product.html',
			resolve: {
				isLoggedIn: checkLogin,
				exists : checkPage
			}
		})
		.when('/:page/:subpage', {
			controller: 'pageController',
			templateUrl: SETTINGS.views() + 'page.html',
			resolve: {
				isLoggedIn: checkLogin,
				exists : checkPage
			}
		})
		.when('/404', {
			controller: 'homeController',
			templateUrl: SETTINGS.views() + 'home.html',
			resolve: {
				isLoggedIn: checkLogin
			}
		})
		.otherwise({
			redirectTo: '/404'
		});
});

checkLogin = function() {
	if (USER.admin) {
		console.log('You\'re loggen in as admin');
	}
	else {
		console.log("You are nobody");
	}
}

checkPage = function($location, $routeParams) {
	console.log($location.path())
	// if ($routeParams.page != "login" || $routeParams.page != "404") {
	// 	$location.path("/404");
	// }
}
