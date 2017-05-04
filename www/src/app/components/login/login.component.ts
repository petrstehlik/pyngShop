import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
<<<<<<< HEAD
import { AuthService, UserService } from 'app/services';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  providers : [AuthService, UserService]
=======
import { AuthService } from 'app/services';

@Component({
  selector: 'login',
  templateUrl: './login.component.html',
  styleUrls: ['./login.component.scss'],
  providers : [AuthService]
>>>>>>> de2c086... Add basic components
})
export class LoginComponent implements OnInit {

	loading = false;
	loginBtn = "Login";
	user = {
		id : "",
		username : "",
		password : "",
		email : ""
	};
	formError = false;
	formErrorMsg = "";
	returnUrl : String;

	constructor(
		private route : ActivatedRoute,
		private router : Router,
<<<<<<< HEAD
		private authService: AuthService,
	    private userService : UserService) {}
=======
		private authService: AuthService) {}
>>>>>>> de2c086... Add basic components

	ngOnInit() {
		// fetch the return URL and use it if set
		this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';

		// check if the user is logged in and if so redirect them to HP
		let lsUser = JSON.parse(localStorage.getItem("currentUser"));

		if (lsUser != null && lsUser['session_id']) {
			this.user = lsUser;
			this.router.navigate([this.returnUrl]);
		}
	}

	setError(msg : string) {
		this.formError = true;
		this.formErrorMsg = msg;
		this.loading = false;
		this.loginBtn = "Login";
	}

	unsetError() {
		this.formError = false;
		this.formErrorMsg = "";
		this.loading = false;
		this.loginBtn = "Login";
	}

	login() {
		// Authenticate the user and redirect them
		this.loading = true;
		this.loginBtn = "Loading...";

		if (this.user.username == "" || this.user.password == "") {
			this.setError("Missing username or password");
			return;
		}

		this.authService.login(this.user.username, this.user.password)
			.subscribe(
				data => {
					this.unsetError();
<<<<<<< HEAD
					this.userService.refresh();
=======
>>>>>>> de2c086... Add basic components
					this.router.navigate([this.returnUrl]);
				},
				error => {
					if (error.status > 499) {
						this.setError("Can't connect to server.");
						return;
					}
					try {
						let body = JSON.parse(error['_body']);
						this.setError(body['message']);
					} catch(err) {
						this.setError("Error logging in.");
					}
				}
			);
	}
}
