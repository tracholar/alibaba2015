# recored 结果记录

## model0
	常数项，用户最后一天对该物品行为量  logistic回归 
	
	训练集F1=1.16, 测试集F1=2.9 
	加权比1:100， C=0.0077
	
	
	全部数据 F1 = 1.8%
	best score 0.017293583882
	best parms {'C': 0.00021544346900318845, 'class_weight': {0: 1, 1: 100}}
	
	best score 0.0202207657264
	best parms {'C': 0.0001, 'class_weight': {0: 1, 1: 70}}
	
	
	best score 0.0171046056146
	best parms {'C': 0.0021544346900318821, 'class_weight': {0: 1, 1: 200}}
	clf parms: -3.2126734833 1.52233247361

	F1      P       R
	1.60    0.91    6.62

			F       T
	N   4576851     2171
	P       282     20
	
	
	根正数据后
	
	best score 0.174855371546
	best parms {'C': 0.0001}
	clf parms: -1.90064635925 1.21963529167

	F1      P       R
	18.96   17.81   20.28

			F       T
	N       456566  1020
	P       869     221


	===== for test =====
			F       T
	N       4567997 10237
	P       869     221

	F1      P       R
	3.83    2.11    20.28
## model1
	常数项，	用户对该物品总行为量，用户最后一天对该物品行为量  logistic回归 
	[-4.57766365] [[ 0.65020026  1.34236491]]
	训练集F1 = 0.94 测试集F1=3.6
	加权比1:100， C=0.0013
	
	利用所有数据，调优发现
	[-2.81781935] [[-0.16534085  1.45092141]]
	F1 = 1.78913738019%
	
	best score 0.016934551864
	best parms {'C': 2.1544346900318823e-05, 'class_weight': {0: 1, 1: 200}}
	clf parms: -1.76501368526 -0.563198009584 1.36522998316

	F1      P       R
	2.02    1.30    4.64

			F       T
	N     4577955   1067 
	P       288     14
	

## model2
	常数项，	用户最后一天行为量，用户最后一天对该分类行为量  logistic回归 
	
	训练集F1 = 1.3， 测试集F1=2.7
	加权比1：100， C=0.046
	
	采用全部数据集后
	[-3.22274269] [[ 1.69565179 -0.21331802]]
	F1 = 2.09%
	加权比1:100，C=0.00021544346900318845
	
	best score 0.0180839420153
	best parms {'C': 0.0021544346900318821, 'class_weight': {0: 1, 1: 200}}
	clf parms: -3.05375335799 1.75200734273 -0.174489993525

	F1      P       R
	1.81    1.02    7.95

			F       T
	N     4576693   2329 
	P       278     24
	
## model3 (和模型2本质相同)
	用户最后一天对物品行为量， 最后一天对该物品/最后一天对该类
	best score 0.0201229461605
	best parms {'C': 0.0001, 'class_weight': {0: 1, 1: 70}}
	
	
	best score 0.0179560337304
	best parms {'C': 0.0021544346900318821, 'class_weight': {0: 1, 1: 200}}
	clf parms: -3.33796542765 1.41771384108 0.73993477003

	F1      P       R
	1.87    1.09    6.62

			F       T
	N   4577204     1818   
	P       282     20

## model4 *
	常数项，	用户最后一天对物品行为量，用户最后一天对该分类行为量，用户转化率 logistic回归 
	
	best score 0.0180369104645
	best parms {'C': 0.0021544346900318821, 'class_weight': {0: 1, 1: 200}}
	clf parms: -3.06113171244 1.7510171625 -0.173875520012 0.697610373863

	F1      P       R
	1.81    1.02    7.95

			F       T
	N    4576690    2332   
	P       278     24
	
## model5
用户最后一天对物品行为量，用户最后一天对该分类行为量，用户转化率，用户总活跃度
	best score 0.0160327716802
	best parms {'C': 0.01, 'class_weight': {0: 1, 1: 200}}
	clf parms: -2.57683509693 1.73799458623 -0.159567672777 3.08319730965 -0.0720672
	891184



	F1      P       R
	1.68    0.95    7.28

			F       T
	N     4576727   2295 
	P       280     22
	
	用户总活跃度没用
	
## model6
用户最后一天对物品行为量，用户最后一天对该分类行为量，用户转化率，商品最后一天热门程度

	best score 0.0181142780741
	best parms {'C': 0.0021544346900318821, 'class_weight': {0: 1, 1: 200}}
	clf parms: -3.04832973967 1.81527178225 -0.174940600552 0.698102032411 -0.065003
	5007965

	F1      P       R
	1.81    1.02    7.95

			F       T
	N    4576702    2320
	P       278     24
	
	商品最后一天热门程度 没有用
	
	将最后一天热门程度改为商品转化率 还是没用
	
	best score 0.0169921514151
	best parms {'C': 0.0021544346900318821, 'class_weight': {0: 1, 1: 200}}
	clf parms: -3.06885170525 1.7466379079 -0.171969799941 0.692126806302 0.849719897682

	F1      P       R
	1.70    0.96    7.62

			F       T
	N       4576638	2384    
	P       279     23
	
## mode7
	特征
	2 user_action_count
	3 user_lastday_count
	4 user_buy_count
	5 item_click_count
	6 item_lastday_count
	7 item_buy_count
	8 cat_click_count
	9 cat_buy_count
	10 user_cat_count
	11 user_cat_lastday_count
	12 user_item_count
	13 user_item_lastday_count
	14 user_add_car
	15 user_add_star
	16 item_added_car
	17 item_added_start
	18 user_item_lasttime


	best score 0.598093712254
	best parms {'C': 1.0}
	clf parms: 0.0 -0.503680755658 -0.0261157564643 0.389699200489 -0.570991174428 0
	.0 -0.199626042298 -0.589764951336 0.700835369893 -0.391130392824 0.177812604406
	 1.63355388487 1.12416907038 0.00315413046176 0.11178421992 1.01544624208 0.0349
	256663566 0.168475029007

	F1      P       R
	60.40   76.26   50.00

			F       T
	N       47      4557
	P       151     151
	
	采样参数控制在0.02左右
	
	best score 0.130854419874
	best parms {'C': 0.69519279617756058}
	clf parms:
	intercept	0.000000
	user_action_count	-0.371763
	user_lastday_count	-0.066816
	user_buy_count	0.331509
	item_click_count	-0.502071
	item_lastday_count	-0.002984
	item_buy_count	-0.457847
	cat_click_count	-0.802509
	cat_buy_count	0.858689
	user_cat_count	-0.260454
	user_cat_lastday_count	0.208004
	user_item_count	1.295417
	user_item_lastday_count	1.064782
	user_add_car	0.031094
	user_add_star	0.109781
	item_added_car	1.082721
	item_added_start	0.036579
	user_item_lasttime	0.030474

	F1      P       R
	13.07   46.00   7.62

			F       T
	N       91405   27
	P       279     23


	===== for test =====
			F       T
	N       4577340 1682
	P       279     23
	F1      P       R
	2.29    1.35    7.62

## model8 
在7的基础上增加了转化率

	best score 0.135714752904
	best parms {'C': 233.57214690901213}
	clf parms:
	intercept       0.402688
	user_action_count       -0.135196
	user_lastday_count      -0.067643
	user_buy_count  0.121783
	item_click_count        -0.557212
	item_lastday_count      -0.047574
	item_buy_count  -0.289825
	cat_click_count -0.823642
	cat_buy_count   0.888391
	user_cat_count  -0.275224
	user_cat_lastday_count  0.207819
	user_item_count 1.351654
	user_item_lastday_count 1.120657
	user_add_car    0.033034
	user_add_star   0.113090
	item_added_car  1.088700
	item_added_start        0.042085
	user_item_lasttime      -0.041916
	item_convert_rate       -5.019174
	user_convert_rate       20.144411




	F1      P       R
	14.25   51.02   8.28

			F       T
	N       91408   24
	P       277     25


	===== for test =====
			F       T
	N       4577224 1798
	P       277     25

	F1      P       R
	2.35    1.37    8.28

## model9
在模型8上又增加了一些特征

	0 user_id
	1 item_id
	2 user_action_count
	3 user_lastday_count
	4 user_buy_count
	5 item_click_count
	6 item_lastday_count
	7 item_buy_count
	8 cat_click_count
	9 cat_buy_count
	10 user_cat_count
	11 user_cat_lastday_count
	12 user_item_count
	13 user_item_lastday_count
	14 user_add_car
	15 user_add_star
	16 item_added_car
	17 item_added_start
	18 user_item_lasttime
	19 cat_add_car
	20 cat_add_star
	21 user_item_buy
	22 user_item_lastweek_click
	23 user_item_lastweek_star
	24 user_item_lastweek_add_car
	25 user_item_lastweek_buy
	26 user_item_halfmonth_click
	27 user_item_halfmonth_star
	28 user_item_halfmonth_add_car
	29 user_item_halfmonth_buy
	30 user_item_before_halfmonth_click
	31 user_item_before_halfmonth_star
	32 user_item_before_halfmonth_add_car
	33 user_item_before_halfmonth_buy
	34 buy
	
	训练结果是
	
	best score 0.284183097713
	best parms {'C': 26.366508987303554}
	clf parms:
	intercept       3.104222
	user_action_count       -0.207504
	user_lastday_count      -0.076293
	user_buy_count  0.242781
	item_click_count        -0.212786
	item_lastday_count      -0.097783
	item_buy_count  0.344305
	cat_click_count -1.224114
	cat_buy_count   0.609725
	user_cat_count  -0.258504
	user_cat_lastday_count  0.077649
	user_item_count 0.332926
	user_item_lastday_count 0.971126
	user_add_car    -0.113400
	user_add_star   0.097122
	item_added_car  0.045578
	item_added_start        0.116045
	user_item_lasttime      0.166021
	cat_add_car     0.563352
	cat_add_star    0.116039
	user_item_buy   -2.159341
	user_item_lastweek_click        0.686702
	user_item_lastweek_star 0.277676
	user_item_lastweek_add_car      1.697815
	user_item_lastweek_buy  0.094305
	user_item_halfmonth_click       0.250627
	user_item_halfmonth_star        -0.413401
	user_item_halfmonth_add_car     0.000000
	user_item_halfmonth_buy 2.074181
	user_item_before_halfmonth_click        -0.002502
	user_item_before_halfmonth_star -0.073459
	user_item_before_halfmonth_add_car      0.007877
	user_item_before_halfmonth_buy  2.615367
	item_convert_rate       -0.535343
	user_convert_rate       14.319559


	F1      P       R
	28.35   63.95   18.21

			F       T
	N       91401   31
	P       247     55


	===== for test =====
			F       T
	N       4576916 2106
	P       247     55

	F1      P       R
	4.47    2.55    18.21
	

### 增加用户和类别的特征

	best score 0.305488138809
	best parms {'C': 0.33598182862837811}
	clf parms:
	intercept       0.000000
	user_action_count       -0.303206
	user_lastday_count      -0.031510
	user_buy_count  0.350275
	item_click_count        -0.157870
	item_lastday_count      -0.011975
	item_buy_count  0.188058
	cat_click_count -0.923669
	cat_buy_count   0.596875
	user_cat_count  -0.375394
	user_cat_lastday_count  0.031611
	user_item_count 0.468305
	user_item_lastday_count 0.873731
	user_add_car    -0.141360
	user_add_star   0.070143
	item_added_car  0.058130
	item_added_start        0.091674
	user_item_lasttime      0.096233
	cat_add_car     0.386160
	cat_add_star    0.000000
	user_item_buy   0.000000
	user_item_lastweek_click        0.626814
	user_item_lastweek_star 0.309774
	user_item_lastweek_add_car      1.248091
	user_item_lastweek_buy  -0.457664
	user_item_halfmonth_click       0.120086
	user_item_halfmonth_star        0.000000
	user_item_halfmonth_add_car     0.000000
	user_item_halfmonth_buy 0.000000
	user_item_before_halfmonth_click        0.039437
	user_item_before_halfmonth_star 0.000000
	user_item_before_halfmonth_add_car      0.000105
	user_item_before_halfmonth_buy  0.000000
	user_cat_lastweek_click 0.055041
	user_cat_lastweek_star  0.000000
	user_cat_lastweek_add_car       0.375398
	user_cat_lastweek_buy   -1.194903
	user_cat_halfmonth_click        0.045370
	user_cat_halfmonth_star 0.000000
	user_cat_halfmonth_add_car      0.039035
	user_cat_halfmonth_buy  0.180086
	user_cat_before_halfmonth_click -0.083721
	user_cat_before_halfmonth_star  0.000000
	user_cat_before_halfmonth_add_car       -0.231196
	user_cat_before_halfmonth_buy   0.666587
	item_convert_rate       0.000000
	user_convert_rate       0.000000


	F1      P       R
	31.79   70.45   20.53

			F       T
	N       91406   26
	P       240     62


	===== for test =====
			F       T
	N       4577134 1888
	P       240     62

	F1      P       R
	5.51    3.18    20.53
	
	======上面的结果有问题=======
	
	固定参数C=1，采样参数为0.05
	
	best score 0.24460316054
	best parms {'C': 1}
	clf parms:
	intercept       0.000000
	user_action_count       -0.412294
	user_lastday_count      -0.004247
	user_buy_count  0.365871
	item_click_count        -0.234662
	item_lastday_count      0.128407
	item_buy_count  0.119019
	cat_click_count -0.597157
	cat_buy_count   0.612829
	user_cat_count  -0.215714
	user_cat_lastday_count  0.131090
	user_item_count 1.159468
	user_item_lastday_count 0.583099
	user_add_car    -0.122665
	user_add_star   0.054486
	item_added_car  0.306778
	item_added_start        -0.048224
	user_item_lasttime      0.172546
	cat_add_car     -0.044878
	cat_add_star    0.016947
	user_item_buy   -1.930079
	user_item_lastweek_click        0.383829
	user_item_lastweek_star 0.382999
	user_item_lastweek_add_car      0.931057
	user_item_lastweek_buy  0.896675
	user_item_halfmonth_click       0.028987
	user_item_halfmonth_star        -0.239761
	user_item_halfmonth_add_car     -0.063565
	user_item_halfmonth_buy 1.454027
	user_item_before_halfmonth_click        -0.215901
	user_item_before_halfmonth_star 0.150459
	user_item_before_halfmonth_add_car      0.160473
	user_item_before_halfmonth_buy  1.563669
	user_cat_lastweek_click 0.096115
	user_cat_lastweek_star  -0.055002
	user_cat_lastweek_add_car       0.146717
	user_cat_lastweek_buy   -0.793438
	user_cat_halfmonth_click        0.014127
	user_cat_halfmonth_star 0.065617
	user_cat_halfmonth_add_car      -0.036352
	user_cat_halfmonth_buy  0.034719
	user_cat_before_halfmonth_click -0.049762
	user_cat_before_halfmonth_star  0.000000
	user_cat_before_halfmonth_add_car       -0.084724
	user_cat_before_halfmonth_buy   0.450901
	item_convert_rate       2.620281
	user_convert_rate       0.000000


	F1      P       R
	25.51   60.69   16.15

			F       T
	N       228466  114
	P       914     176


	===== for test =====
			F       T
	N       4575544 2690
	P       914     176

	F1      P       R
	8.90    6.14    16.15
	
	
	分开训练集和测试集

	best score 0.221799101661
	best parms {'C': 0.31622776601683794}
	clf parms:
	intercept       0.000000
	user_action_count       -0.441908
	user_lastday_count      -0.015867
	user_buy_count  0.303836
	item_click_count        -0.210976
	item_lastday_count      0.031571
	item_buy_count  0.038037
	cat_click_count -0.517445
	cat_buy_count   0.690812
	user_cat_count  -0.171438
	user_cat_lastday_count  0.150967
	user_item_count 1.140760
	user_item_lastday_count 0.614176
	user_add_car    -0.057524
	user_add_star   0.082944
	item_added_car  0.349464
	item_added_start        0.000000
	user_item_lasttime      0.043606
	cat_add_car     -0.172854
	cat_add_star    -0.007370
	user_item_buy   -0.602371
	user_item_lastweek_click        0.365752
	user_item_lastweek_star 0.343867
	user_item_lastweek_add_car      0.809786
	user_item_lastweek_buy  0.000000
	user_item_halfmonth_click       0.046286
	user_item_halfmonth_star        -0.100908
	user_item_halfmonth_add_car     -0.032098
	user_item_halfmonth_buy 0.137501
	user_item_before_halfmonth_click        -0.215836
	user_item_before_halfmonth_star 0.000000
	user_item_before_halfmonth_add_car      0.000000
	user_item_before_halfmonth_buy  0.555807
	user_cat_lastweek_click 0.127782
	user_cat_lastweek_star  -0.031270
	user_cat_lastweek_add_car       0.119557
	user_cat_lastweek_buy   -0.725741
	user_cat_halfmonth_click        -0.060077
	user_cat_halfmonth_star -0.036643
	user_cat_halfmonth_add_car      -0.054867
	user_cat_halfmonth_buy  0.143869
	user_cat_before_halfmonth_click -0.060219
	user_cat_before_halfmonth_star  0.000000
	user_cat_before_halfmonth_add_car       -0.031587
	user_cat_before_halfmonth_buy   0.434426
	item_convert_rate       0.000000
	user_convert_rate       0.000000




	F1      P       R
	22.14   56.79   13.75

			F       T
	N       136833  70
	P       577     92


	===== for test =====
			F       T
	N       1831407 1032
	P       351     70

	F1      P       R
	9.19    6.35    16.63
	
	
	
#### ====== 记录=======
	best score 0.228346300866
	best parms {'C': 10.0}
	clf parms:
	intercept       -0.057189
	user_action_count       -0.521748
	user_lastday_count      -0.008182
	user_buy_count  0.414034
	item_click_count        -0.190652
	item_lastday_count      0.083779
	item_buy_count  0.155922
	cat_click_count -0.610941
	cat_buy_count   0.749927
	user_cat_count  -0.502132
	user_cat_lastday_count  0.326462
	user_item_count 4.166696
	user_item_lastday_count 0.681126
	user_add_car    -0.121371
	user_add_star   0.093671
	item_added_car  0.226864
	item_added_start        -0.050703
	user_item_lasttime      -0.001870
	cat_add_car     -0.197033
	cat_add_star    0.037219
	user_item_buy   -0.499866
	user_item_lastweek_click        0.000000
	user_item_lastweek_star 0.000000
	user_item_lastweek_add_car      0.000000
	user_item_lastweek_buy  0.000000
	user_item_halfmonth_click       0.000000
	user_item_halfmonth_star        0.000000
	user_item_halfmonth_add_car     0.000000
	user_item_halfmonth_buy 0.000000
	user_item_before_halfmonth_click        -2.416822
	user_item_before_halfmonth_star -0.211741
	user_item_before_halfmonth_add_car      0.018093
	user_item_before_halfmonth_buy  -0.362747
	user_cat_lastweek_click 0.000000
	user_cat_lastweek_star  0.000000
	user_cat_lastweek_add_car       0.000000
	user_cat_lastweek_buy   0.000000
	user_cat_halfmonth_click        0.000000
	user_cat_halfmonth_star 1.145733
	user_cat_halfmonth_add_car      0.000000
	user_cat_halfmonth_buy  0.000000
	user_cat_before_halfmonth_click 0.287978
	user_cat_before_halfmonth_star  0.072676
	user_cat_before_halfmonth_add_car       0.147421
	user_cat_before_halfmonth_buy   -0.120659
	user_lastday_add_star   -0.024881
	user_item_lastday_add_star      0.347383
	user_cat_lastday_add_star       -0.251742
	user_lastday_add_cart   0.037017
	user_item_lastday_add_cart      0.861920
	user_cat_lastday_add_cart       -0.132907
	user_lastday_buy        -0.130404
	user_item_lastday_buy   -0.640501
	user_cat_lastday_buy    -0.594544
	item_convert_rate       0.402244
	user_convert_rate       1.084939


	F1      P       R
	22.33   56.71   13.90

			F       T
	N       136832  71
	P       576     93


	===== for test =====
			F       T
	N       1831380 1059
	P       349     72

	F1      P       R
	9.28    6.37    17.10
	
	
## model10

	best score 0.224867666147
	best parms {'C': 5.9948425031894086}
	clf parms:
	intercept       -0.137796
	user_action_count       -0.530330
	user_lastday_count      -0.008653
	user_buy_count  0.425831
	item_click_count        -0.185507
	item_lastday_count      0.079314
	item_buy_count  0.176756
	cat_click_count -0.609604
	cat_buy_count   0.737831
	user_cat_count  -0.452063
	user_cat_lastday_count  0.327599
	user_item_count 4.166340
	user_item_lastday_count 0.690345
	user_add_car    -0.122329
	user_add_star   0.092889
	item_added_car  0.218570
	item_added_start        -0.068368
	user_item_lasttime      -0.058002
	cat_add_car     -0.184029
	cat_add_star    0.032016
	user_item_buy   -0.521416
	user_item_lastweek_star 0.377425
	user_item_before_halfmonth_click        -2.412691
	user_item_before_halfmonth_star -0.449780
	user_item_before_halfmonth_add_car      -0.137746
	user_item_before_halfmonth_buy  -0.416321
	user_cat_lastweek_star  0.371491
	user_cat_halfmonth_buy  0.040139
	user_cat_before_halfmonth_click 0.238205
	user_cat_before_halfmonth_star  0.074419
	user_cat_before_halfmonth_add_car       0.139552
	user_cat_before_halfmonth_buy   -0.109298
	user_lastday_add_star   -0.023306
	user_item_lastday_add_star      0.333326
	user_cat_lastday_add_star       -0.254875
	user_lastday_add_cart   0.035361
	user_item_lastday_add_cart      0.827894
	user_cat_lastday_add_cart       -0.136018
	user_lastday_buy        -0.127181
	user_item_lastday_buy   -0.647401
	user_cat_lastday_buy    -0.613243
	item_convert_rate       -0.252983
	user_item_click_nobuy   0.210148
	user_item_star_nobuy    0.407423
	user_item_cart_nobuy    0.326381
	user_item_buy_again     0.925407


	F1      P       R
	22.30   56.36   13.90

			F       T
	N       136831  72
	P       576     93


	===== for test =====
			F       T
	N       1831380 1059
	P       351     70

	F1      P       R
	9.03    6.20    16.63