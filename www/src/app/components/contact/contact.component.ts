import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'app-contact',
  templateUrl: './contact.component.html',
  styleUrls: ['./contact.component.scss']
})
export class Contact {

	constructor(
	public username : string,
	public firstname : string,
	public lastname : string,
	public password : string,
	public email : string,
	public address : string,
	public city : string,
	public postalcode : number,
	public phone : number,
	public country : string
	) {  }
}
