import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CustomerAuthService } from 'app/services/customer-auth.service';
import { Contact} from 'app/components/contact/contact.component'
import { CustomFormsModule } from 'ng2-validation'

@Component({
  selector: 'app-account',
  templateUrl: './account.component.html',
  styleUrls: ['./account.component.scss'],
  providers: [CustomerAuthService]
})
export class AccountComponent implements OnInit {
	user = new Contact('', '', '', '', '', '', '', 0, +421, '');
	constructor(private customerService : CustomerAuthService, private router : Router) { }
	submitted = false;

	ngOnInit() {
		this.customerService.checkSession().subscribe(
			data => {
				console.debug("Session data")
				console.log(data);
				this.user = JSON.parse(localStorage.getItem('currentUser'));
				console.debug("PArsed user");
				console.log(this.user);
			},
			err => {
				console.log(err);
			}
		);
	}

	onSubmit() {
		console.debug("Submit user");
		console.log(this.user);
		this.submitted = true;
		this.customerService.update(this.user).subscribe(
			data => {
				localStorage.setItem('currentUser', JSON.stringify(this.user));
			},
			err => {
				console.log(err);
				this.submitted = false;
			}
		);
		// Push to local storage
		//localStorage.setItem('currentUser', JSON.stringify(this.user));
	}

}
