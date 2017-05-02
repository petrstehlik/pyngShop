import { Injectable } from '@angular/core';
import { Http, Headers, RequestOptions, Response } from '@angular/http';
import { Observable } from 'rxjs/Observable';
import 'rxjs/add/operator/map';

import { UserService } from 'app/services/user.service';

@Injectable(
)
export class CustomerAuthService {

	constructor(private http: Http,
	           private userService : UserService) { }

	login(username: string, password: string) {
		return this.http.post('/authorization/customer',
			JSON.stringify({ username: username, password: password })
			)
            .map((response: Response) => {
                // login successful
				let resp = response.json();

				if (resp && resp['error']) {
					console.error(resp['error']);
					return;
				}

				console.debug(resp)

				if (resp) {
                    // store user details and token in local storage to keep user logged in between page refreshes
                    localStorage.setItem('currentUser', JSON.stringify(resp));
                    this.userService.refresh();
                }
			})
			.catch(this.handleError);
    }

    logout() {
		// remove user from local storage to log user out
		let user = JSON.parse(localStorage.getItem('currentUser'));
		console.log(user);
		return this.http.delete('/authorization')
			.map((response : Response) => {
				console.log(response);
				this.userService.refresh();
			}).catch(this.handleError);
			//localStorage.removeItem('currentUser');

	}

	register(customer : Object) {
		return this.http.post('/customers', JSON.stringify(customer))
		.map((response : Response) => {
			console.log(response);
		}).catch(this.handleError);
	}

	update(customer : Object) {
		return this.http.put('/profile', JSON.stringify(customer))
		.map((response : Response) => {
			console.log(response);
		}).catch(this.handleError);
	}

	checkSession() {
		return this.http.get('/authorization').map(
			(response : Response) => {
				console.debug('Session is valid');
			})
			.catch(this.handleError);
	}

    admin(user : Object) {
        return this.http.post('/setup'
            , JSON.stringify(user))
            .map(
            (resp : Response) => {
                console.debug("Admin inserted");
            })
            .catch(this.handleError);
    }

	private handleError(err : Response | any) {
	    console.log(err);
		return Promise.reject(err);
	}
}
