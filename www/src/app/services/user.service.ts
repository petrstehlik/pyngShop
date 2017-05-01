import { Injectable } from '@angular/core';
<<<<<<< HEAD
=======
import { AuthService } from './auth.service';
>>>>>>> 6162472... Service: operations with user

@Injectable()
export class UserService {
    user : Object;

<<<<<<< HEAD
    constructor() {
        this.refresh();
    }

    refresh() {
        this.user = JSON.parse(localStorage.getItem('currentUser'));

        if (this.user == null) {
=======
    constructor(private auth : AuthService) {
        this.user = JSON.parse(localStorage.getItem('currentUser'));

        if (this.user == undefined) {
>>>>>>> 6162472... Service: operations with user
            console.warn("No user found");
        }
    }

    current() : Object {
        return this.user;
    }

    isAdmin() {
<<<<<<< HEAD
		if (this.user == null)
        		return false;
=======
>>>>>>> 6162472... Service: operations with user
        try {
            return this.user["user"]["role"] === 0;
        } catch(e) {
            return false;
        }
    }

    isCustomer() {
        try {
<<<<<<< HEAD
        	if (this.user == null)
        		return false;
			return this.user["customer"]["role"] > 9;
        } catch(e) {
			return false;
=======
            return this.user["user"]["role"] > 9;
        } catch(e) {
            return false;
>>>>>>> 6162472... Service: operations with user
        }
    }

    isGuest() {
        return(this.user == undefined);
    }

}
