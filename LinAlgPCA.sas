libname linalg "C:\Users\sydne\Documents\Linear Algebra";

proc princomp data=linalg.testscores out=testPCs cov;
var _all_;
run;
/*in output for this: 
you get the mean and sd of each variable. 
then you get the correlation matirx. THE DEFAULT PCA METHOD IS CORRELATION IN SAS
THEN you get the eigenvalues of the correlation matrix.
the first eigen value gives you the variance of the first principal component.
the proportion gives the prop of var explained by that eigenvalue
then you get the scree plot and the prop of var explained
then you get the eigen vectors which gives the loadings of each test on each component
in this example, you see that the first principal component has big numbers for the middle 3 tests
because these tests had the greatest variance so thats good! The second principal component
is equal to -.8test1 + .14test2 + .07test3 +.15test4+.5test5 : the interpreation of this is
that the relative contirubution of the middle three tests are small compared to the other 
two. so what if we drop them? then we get -.8test1+.5test5 or .5test5-.8test1 so the interpretation 
of this componed could be the difference between test 5 and test 1. so the negative values on prin2 are the 
people that did better on test 1 than test 5. 
*/

proc sgplot data=testPCs;
	scatter x=Prin1 y=Prin2;
run;

