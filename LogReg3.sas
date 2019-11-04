libname logr "C:\Users\sydne\Documents\Logistic Regression\Homework2_LR";


data logreg2;
	set logr.insurance_t_bin;
run;

proc print data=logreg2 (obs=100);
run;

%let predictors = DDA	CASHBK	DIRDEP	NSF	SAV	ATM	CD	IRA	LOC	ILS	MM	MMCRED	MTG	SDB	MOVED	
				INAREA	BRANCH	RES	DDABAL_Bin	ACCTAGE_Bin	DEPAMT_Bin	CHECKS_Bin	NSFAMT_Bin	
				PHONE_Bin	TELLER_Bin	SAVBAL_Bin	ATMAMT_Bin	POS_Bin	POSAMT_Bin	CDBAL_Bin	
				IRABAL_Bin	LOCBAL_Bin	INVBAL_Bin	ILSBAL_Bin	MMBAL_Bin	MTGBAL_Bin	CCBAL_Bin	
				INCOME_Bin	LORES_Bin	HMVAL_Bin AGE_Bin	CRSCORE_Bin	INV2 CC2 CCPURC2 HMOWN2;
				

proc means data=logreg2 nmiss;
run;


data logreg2;	
	set logreg2;
	INV2 =put(INV,1.);
	CC2 = put(CC,1.);
	CCPURC2 = put(CCPURC,1.);
	HMOWN2 = put(HMOWN,1.);
	if INV2 = . then INV2 = "M";
	if CC2 = . then CC2 = "M";
	if CCPURC2 = . then CCPURC2 = "M";
	if HMOWN2 = . then HMOWN2 = "M";
	drop INV CC CCPURC HMOWN;
run;

/*** check to see if values have been recoded correctly and checking for complete seperation ***/
/******************************************************************************************************
*  Objective 2:Check each variable for separation concerns. Document in the report and adjust any     *
*  variables with complete or quasi-separation concerns                                               *
******************************************************************************************************/
proc freq data=logreg2 nlevels;
	tables INS*(&predictors.) / nocol norow nocum nopercent;
run;

/*************************************************
*Complete Seperation:                            *
*Quasai Complete Seperation: CASHBK MMCRED       *
                                                 *
Solution: Recode CASHBK = 2 to CASHBK = 1        *
		  Recode MMCRED = 5 to MMCRED = 3        *
*************************************************/

proc freq data=logreg2;
	tables INS*(CASHBK MMCRED);
run;

data logreg2;
	set logreg2;
	if CASHBK = 2 then CASHBK = 1;
	if MMCRED = 5 then MMCRED = 3;
run;

proc freq data=logreg2;
	tables INS*(CASHBK MMCRED);
run;


/******************************************************************************************************
*Objective 3: Use backward selection to do the variable selection â€“ the Bank currently uses           *
* alpha = 0.002and p-values to perform backward, but is open to another technique and/or significance *
* level if documented in your report.                                                                 *
*Objective 4: Report the final variables from this model ranked by p-value.                           *
******************************************************************************************************/

proc logistic data=logreg2 plots(only)=(oddsratio);
	class &predictors. / param=ref;
	model INS(event='1') = &predictors. / selection=backward slstay = .002
										  clodds = pl clparm = pl;
run;

%let sigpred = DDA 	 NSF  IRA  ILS  MM  MTG  DDABAL_Bin  
    CHECKS_Bin  TELLER_Bin  SAVBAL_Bin  ATMAMT_Bin  CDBAL_Bin  
    INV2  CC2  DDA:IRA;




/******************************************************************************************************
* Objective 6: Investigate possible interactions using forward selection including only the main      *
* effects from your previous final model. 															  *
******************************************************************************************************/


proc logistic data=logreg2 plots(only)=(oddsratio);
	class &sigpred. /param=ref;
	model INS(event='1') = &sigpred. DDA|NSF|IRA|ILS|MM|DDABAL_Bin|CHECKS_Bin|Teller_Bin
									 |SAVBAL_Bin|ATMAMT_Bin|CDBAL_Bin|INV2|CC2 @2 / selection=forward slentry=.002;
run;



/******************************************************************************************************
* HOMEWORK 3																						  *
******************************************************************************************************/


/******************************************************************************************************
* Objective 1: Report and interpret the following probability metrics for your model on training data. *
o Concordance percentage.																			   *	
o Discrimination slope – provide the coefficient of discrimination as well as a visual                 * 
representation through histograms.																	   *					  *
******************************************************************************************************/

%let sigpred = DDA 	 NSF  IRA  ILS  MM  MTG  DDABAL_Bin  
    CHECKS_Bin  TELLER_Bin  SAVBAL_Bin  ATMAMT_Bin  CDBAL_Bin  
    INV2  CC2  DDA:IRA;


proc logistic data = logreg2 plots(only)=(oddsratio);
	class &sigpred. ;
	model INS(event='1')=&sigpred.;
run;
	
proc logistic data=logreg2 noprint;
	class &sigpred.;
	model INS(event='1') = &sigpred.;
	output out=predprobs p=phat;
run;

proc sort data=predprobs;
by descending INS;
run;

proc ttest data=predprobs order=data;
ods select statistics summarypanel;
class INS;
var phat;
title 'Coefficient of Discrimination and Plots';
run;



/* concordance: .8 
	discrimination slope: .2461? */


/******************************************************************************************************
Report and interpret the following classification metrics for your model on training data.
o Visually show the ROC curve.
 (HINT: Although this is one of the only times I will allow SAS output in a report,
make sure the axes and title are well labeled.)
o K-S Statistic. The Bank currently uses the K-S statistic to choose the threshold for
classification but are op																   *					  *
******************************************************************************************************/


/* ROC Curve */
proc logistic data=logreg2 plots(only)=ROC;
	class &sigpred. ;
	model INS(event='1') = &sigpred. / clodds=pl clparm=pl;
	title 'Modeling Insurance Product Purchase';
run;
quit;

/*K-S Statistic*/
proc logistic data=logreg2 noprint;
	class &sigpred.;
	model INS(event='1') = &sigpred. / clodds=pl clparm=pl;
	output out=predprobs p=phat;
run;

proc npar1way data=predprobs d plot=edfplot;
	class INS;
	var phat;
run;
/*D=0.4729*/



/******************************************************************************************************
Report and interpret the following classification metrics for your model on validation data.
o Display your final confusion matrix.
o Accuracy.
o Lift – add a visual to help show the model performance														   *					  *
******************************************************************************************************/
/* Lift Chart */
proc logistic data=logreg2 plots(only)=(oddsratio);
	class &sigpred. ; 
	model INS(event='1') = &sigpred./ clodds=pl clparm=pl;
	score data=logreg2 fitstat outroc=roc; *scoring own dataset and using outroc=roc to get output from roc curve;
	title 'Modeling Insurance Product Purchase';
run;
quit;


data work.roc; 
	set work.roc; 
	cutoff = _PROB_; 
	specif = 1-_1MSPEC_; 
	depth=(_POS_+_FALPOS_)/8495*100; 
	precision=_POS_/(_POS_+_FALPOS_); 
	acc=_POS_+_NEG_; 
	lift=precision/0.3435;    *pop%of ones in dataset!!;
run;

proc sgplot data=work.roc; 
	*where 0.005 <= depth <= 0.50; 
	series y=lift x=depth; 
	refline 1.0 / axis=y; 
	title1 "Lift Chart for Training Data"; 
	xaxis label="Depth (%)";
	yaxis label="Lift";
run; 
quit;

/*Classification Table/Confusion Matirx*/

proc logistic data=logreg2 plots(only)=(oddsratio);
	class &sigpred.; 
	model INS(event='1') = &sigpred./ ctable pprob = 0 to 0.98 by 0.02; *ctable give confusion matirx;
	ods output classification=classtable;
	title 'Modeling Low Birth Weight';
run;
quit;

*look at sensitivty and specificity. then use a data step on the ods output dataset;

/* Youden's Index */
data classtable;
	set classtable;
	youden = sensitivity + specificity - 100; *calculating J;
	drop PPV NPV Correct;
run;

proc sort data=classtable;
	by descending youden; *sort to get highest index, look at problevel column to get optimized cutoff level. , now you can look closer (not jump by.02) ;
run;

proc print data=classtable;
run;