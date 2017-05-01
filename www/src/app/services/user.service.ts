import { Injectable } from '@angular/core';

@Injectable()
export class UserService {
    user : Object;

    constructor() {
        this.refresh();
    }

    refresh() {
        this.user = JSON.parse(localStorage.getItem('currentUser'));
        console.log("refresh has been called", this.user);

        if (this.user == null) {
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
