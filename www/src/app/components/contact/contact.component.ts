import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.scss']
})
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
