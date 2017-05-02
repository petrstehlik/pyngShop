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
	lsUser = null;
	constructor(private customerService : CustomerAuthService, private router : Router) { }
	submitted = false;
	message = null;

	ngOnInit() {
		this.customerService.fetch().subscribe(
			data => {
				this.user = data;
				this.lsUser = JSON.parse(localStorage.getItem('currentUser'));
				this.lsUser["customer"] = this.user;
				localStorage.setItem('currentUser', JSON.stringify(this.lsUser));
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
		this.message = null;
		this.customerService.update(this.user).subscribe(
			data => {
				this.user = data;
				this.lsUser = JSON.parse(localStorage.getItem('currentUser'));
				this.lsUser["customer"] = this.user;
				localStorage.setItem('currentUser', JSON.stringify(this.lsUser));
				this.message = "Update successfull";
			},
			err => {
				console.log(err);
				this.message = err["message"];
				this.submitted = false;
			}
		);
		// Push to local storage
		//localStorage.setItem('currentUser', JSON.stringify(this.user));
	}

}
