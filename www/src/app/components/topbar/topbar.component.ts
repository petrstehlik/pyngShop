import { Component, OnInit } from '@angular/core';
<<<<<<< HEAD
import { Router, ActivatedRoute } from '@angular/router';

import { UserService, CartService, AuthService } from 'app/services';
=======
>>>>>>> de2c086... Add basic components

@Component({
  selector: 'topbar',
  templateUrl: './topbar.component.html',
<<<<<<< HEAD
  styleUrls: ['./topbar.component.scss'],
  providers : [UserService, CartService, AuthService]
})
export class TopBarComponent implements OnInit {

    constructor(private user : UserService,
                private cart : CartService,
                private auth : AuthService,
                private route : ActivatedRoute,
                private router : Router) { }

    ngOnInit() {}

    logout() {
        this.auth.logout()
            .subscribe(
                data => {
                    console.log('Success logging out.');
                    localStorage.removeItem("currentUser");
                    this.user.refresh();
                    this.router.navigate(["/"]);
                },
                error => {
                    console.log('Error logging out.');
                    localStorage.removeItem("currentUser");
                    //this.router.navigate([this.returnUrl]);
                }
            );
    }
=======
  styleUrls: ['./topbar.component.scss']
})
export class TopBarComponent implements OnInit {

	role = {
		"admin" : true
	}

  constructor() { }

  ngOnInit() {
  }
>>>>>>> de2c086... Add basic components

}
