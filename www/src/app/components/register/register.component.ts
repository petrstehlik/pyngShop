import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
//import { Contact} from 'app/components/contact/contact.component'
import { CustomerAuthService } from 'app/services/customer-auth.service';
import { CustomFormsModule } from 'ng2-validation'

export class Contact {

	constructor(
	public username : string,
	public first_name : string,
	public last_name : string,
	public password : string,
	public email : string,
	public address1 : string,
	public city : string,
	public postal_code : number,
	public telephone : number,
	public country : string
	) {  }
}

@Component({
  selector: 'app-register',
  templateUrl: './register.component.html',
  styleUrls: ['./register.component.scss'],
  providers: [CustomerAuthService]
})

export class RegisterComponent implements OnInit {
	contact = new Contact('', '', '', '', '', '', '', 0, 0, '');
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
			err => {console.log(err); this.submitted = false;}
		);
	}

	newContact() {
		this.contact = new Contact('', '', '', '', '', '', '', 0, 0, '');
		this.active = false;
		this.submitted = false;
		setTimeout(()=> this.active=true, 0);
	}

}
