import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'topbar',
  templateUrl: './topbar.component.html',
  styleUrls: ['./topbar.component.scss']
})
export class TopBarComponent implements OnInit {

	role = {
		"admin" : true
	}

  constructor() { }

  ngOnInit() {
  }

}
