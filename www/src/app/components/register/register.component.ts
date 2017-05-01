import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CustomerAuthService } from 'app/services/customer-auth.service';
import { Contact} from 'app/components/contact/contact.component'

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
  providers: [CustomerAuthService]
})

export class RegisterComponent implements OnInit {
	contact = new Contact('testuser', 'Test', 'User', 'test', 'test@user.eu', '', '', '', 0, '');
	submitted = false;
	active = true;

	// dependencies
	constructor(private customer : CustomerAuthService, private router : Router) { }

	ngOnInit() {
	}

	onSubmit() {
		this.submitted = true;
		this.customer.register(this.contact).subscribe(
			data => {this.router.navigate(['/login'])},
			err => {console.log(err); this.submitted = false}
		);
	}

	newContact() {
		this.contact = new Contact('', '', '', '', '', '', '', '', +421, '');
		this.active = false;
		this.submitted = false;
		setTimeout(()=> this.active=true, 0);
	}

}
