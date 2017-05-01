import { Component, OnInit } from '@angular/core';

@Component({
  selector: 'category-bar',
  templateUrl: './category-bar.component.html',
  styleUrls: ['./category-bar.component.scss']
})
export class CategoryBarComponent implements OnInit {

    user = {
        admin : false
    }
    categories = [
        {
            "slug" : "ebooks",
            "name" : "Ebooks",
            "sub" : [
                {
                    "slug" : "beletry",
                    "name" : "Beletry"
                }
            ]

        }
    ]

  constructor() { }

  ngOnInit() {
  }

}
