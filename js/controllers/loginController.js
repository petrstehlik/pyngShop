app.controller('loginController', function($scope, $cookieStore, $location, api, auth){
	$scope.registerSwitch = 0;

	$cookieStore.put('yourCookie', 'hellp')
	var tmp =  $cookieStore.get('yourCookie')
	console.log(tmp)

	$scope.checkLogin = function(login) {
		console.log(login);

		//check if admin
		api.post("login", login).then(function(r) {
			console.log(r)
			var expireDate = new Date();
			expireDate.setDate(expireDate.getDate() + 30);
			if (r.admin || r.customer) {
				auth.store(r, expireDate);
				$location.path('/')
			}
		});
	}

	$scope.register = function(form) {
		console.log(form);
		api.post("register", form).then(function(r) {
			console.log(r)
			$scope.register.form = {}
		})
	}

	$scope.registerToggle = function() {
		console.log("switching to register form")
		$scope.registerSwitch = 1;
	}

	$scope.toggleLogin = function() {
		$scope.registerSwitch= 0;
	}
	
})