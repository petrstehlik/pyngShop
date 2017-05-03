import { Injectable } from '@angular/core';

@Injectable()
export class UserService {
    user : Object;

    constructor() {
        this.refresh();
    }

    refresh() {
        this.user = JSON.parse(localStorage.getItem('currentUser'));

        if (this.user == null) {
            console.warn("No user found");
        }
    }

    current() : Object {
        return this.user;
    }

    isAdmin() {
		if (this.user == null)
        		return false;
        try {
            return this.user["user"]["role"] === 0;
        } catch(e) {
            return false;
        }
    }

    isCustomer() {
        try {
        	if (this.user == null)
        		return false;
			return this.user["customer"]["role"] > 9;
        } catch(e) {
			return false;
        }
    }

    isGuest() {
        return(this.user == undefined);
    }

}
