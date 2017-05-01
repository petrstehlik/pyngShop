import { Component, OnInit, Input } from '@angular/core';

@Component({
  selector: 'category-item',
  templateUrl: './category-item.component.html',
  styleUrls: ['./category-item.component.scss']
})
export class CategoryItemComponent implements OnInit {

    @Input() item : Object;
    user = {
        admin: false
    }

  constructor() { }

  ngOnInit() {
      console.log(this.item);
  }

}
