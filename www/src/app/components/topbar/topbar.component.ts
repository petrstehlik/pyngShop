import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';

import { UserService, CartService, AuthService } from 'app/services';

@Component({
  selector: 'topbar',
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.scss'],
  providers : [UserService, CartService, AuthService]
})
export class TopBarComponent implements OnInit {

    constructor(private user : UserService,
                private cart : CartService,
                private auth : AuthService,
                private route : ActivatedRoute,
                private router : Router) { }

    ngOnInit() {

        console.log(this.route.snapshot.url.toString())
    }

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

}
