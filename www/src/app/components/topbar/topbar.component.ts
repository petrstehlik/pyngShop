import { Component, OnInit } from '@angular/core';
import { UserService } from 'app/services/user.service';
import { CartService } from 'app/services/cart.service';

@Component({
  selector: 'topbar',
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.scss'],
  providers : [UserService, CartService]
})
export class TopBarComponent implements OnInit {

    constructor(private user : UserService,
               private cart : CartService) { }

    ngOnInit() {
    }

}
