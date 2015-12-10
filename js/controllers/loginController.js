app.controller('loginController', function($scope, $location, api, auth, page){
	$scope.registerSwitch = 0;
	$scope.loginbtn = "Log In";
	$scope.login = {};

	page.setTitle("Login");

	$scope.checkLogin = function(login) {
		//console.log(login);
		$scope.loginbtn = "Logging in...";

		//check if admin
		api.post("login", login).then(function(r) {
			//console.log(r)
			var expireDate = new Date();
			expireDate.setDate(expireDate.getDate() + 30);
			if (r.admin) {
				USER.admin = true;
				//console.log(USER)
			}
			if (r.admin || r.customer) {
				auth.store(r, expireDate);
				// $location.path('/');
				history.back();
			} else {
				$scope.error = "Wrong password!";
				$scope.loginbtn = "Log In";
				$scope.login["password"] = "";
			}
		});
	}

	$scope.register = function(form) {
		console.log(form);
		api.post("register", form).then(function(r) {
			console.log(r)
			$scope.register.form = {}
			var expireDate = new Date();
			expireDate.setDate(expireDate.getDate() + 30);
			//auth.store({form}, expireDate);
			$location.path("/");
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

app.controller('accountController', function($scope, $location, auth, api){
	if (!auth.user.customer) {
		$location.path("/")
	}

	$scope.user = auth.user;

	// console.log(auth.user, auth.)

	api.post("customerorders", auth.user.cred.details.customer_id).then(function(r) {
		$scope.orders = r;
	})
})