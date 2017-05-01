import { Injectable } from '@angular/core';
import { AuthService } from './auth.service';

@Injectable()
export class UserService {
    user : Object;

    constructor(private auth : AuthService) {
        this.user = JSON.parse(localStorage.getItem('currentUser'));

        if (this.user == undefined) {
            console.warn("No user found");
        }
    }

    current() : Object {
        return this.user;
    }

    isAdmin() {
        try {
            return this.user["user"]["role"] === 0;
        } catch(e) {
            return false;
        }
    }

    isCustomer() {
        try {
            return this.user["user"]["role"] > 9;
        } catch(e) {
            return false;
        }
    }

    isGuest() {
        return(this.user == undefined);
    }

}
