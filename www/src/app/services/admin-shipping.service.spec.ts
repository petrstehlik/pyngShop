import { TestBed, inject } from '@angular/core/testing';

import { AdminShippingService } from './admin-shipping.service';

describe('AdminShippingService', () => {
  beforeEach(() => {
    TestBed.configureTestingModule({
      providers: [AdminShippingService]
    });
  });

  it('should ...', inject([AdminShippingService], (service: AdminShippingService) => {
    expect(service).toBeTruthy();
  }));
});
