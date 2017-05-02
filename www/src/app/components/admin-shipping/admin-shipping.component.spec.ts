import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { AdminShippingComponent } from './admin-shipping.component';

describe('AdminShippingComponent', () => {
  let component: AdminShippingComponent;
  let fixture: ComponentFixture<AdminShippingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ AdminShippingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(AdminShippingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
