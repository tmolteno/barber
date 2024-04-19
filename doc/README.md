## How Barber works

This is a crazy simple algorithm that treats the visibilities as a single block of numbers. Barber simply computes percentiles to characterise the distribution, and then reports the largest visibility. It works if there are visible fringes across the image. That's it. Nothing more.


## Existing similar techniques

The SVD technique described by Offringa [Offringa, A., MNRAS, 405, 155-167, 2010] seems promising, in that the largest singular values are assumed to be the cause of the RFI. It's elegant. It also assumes that the RFI has to dominate the astronomical signal (I.e., the largest singular values correspond to the RFI.



### Alternatives

* https://doi.org/10.3390/rs12203433 Using  (in a different regime) cross-validation.
* Harrison K & Mishra A. Supervised NN for RFI flagging.
* GRIDflag [Sekhar, Srikrishna, and Ramana Athreya. "Two procedures to flag radio frequency interference in the uv plane." The Astronomical Journal 156.1 (2018): 9.] A nice technique that looks for outliers in a UV bin.

