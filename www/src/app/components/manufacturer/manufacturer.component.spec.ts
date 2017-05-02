import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { Manufacturer } from './manufacturer.component';

describe('ManufacturerComponent', () => {
  let component: Manufacturer;
  let fixture: ComponentFixture<Manufacturer>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ Manufacturer ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(Manufacturer);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
