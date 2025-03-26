--分次产品判断，如果产品代码长度大于11位，就是分次产品
--c_fundcode 主产品内部代码 
-- F_ORDERFACTCOLLECTBALA 发行规模
SELECT h.c_fundcode, h.F_ORDERFACTCOLLECTBALA  FROM  TPDTORDERINFO h  WHERE  h.C_PRDCODEORDER = '10924000112A1';
--TPDTBASICINFO C_PRDREGNO 登记编码
-- d_accessstoredate 登记时间
--TPDTBATCHINFO C_TRUSTEE 产品托管人
select a.C_PRDREGNO,TO_CHAR (b.d_accessstoredate,'yyyy-mm-dd') as d_accessstoredate,
 d.mem_name
FROM TPDTBASICINFO a ,TPDTOPERATEINFO b,TPDTBATCHINFO c,member.member_info d WHERE a.C_FUNDCODE = b.C_FUNDCODE and  a.C_FUNDCODE = c.C_FUNDCODE and c.c_trustee = d.mem_code and a.C_FUNDCODE = '000L7Y';




--第一步：先判断是否是分级产品
--C_FUNDCODE 主产品内部代码
--F_CLASSFACTBALE 发行规模   单位是元
SELECT  G.C_FUNDCODE,G.F_CLASSFACTBALE  FROM TFUNDINFO A,TPDTPRDCLASSINFO G  WHERE A.C_FUNDCODE = G.C_FUNDCODE AND G.C_TAFUNDCODE = '10924000071';
--TPDTBASICINFO C_PRDREGNO 登记编码
-- d_accessstoredate 登记时间
--TPDTBATCHINFO C_TRUSTEE 产品托管人
select a.C_PRDREGNO,TO_CHAR (b.d_accessstoredate,'yyyy-mm-dd') as d_accessstoredate,
 d.mem_name
FROM TPDTBASICINFO a ,TPDTOPERATEINFO b,TPDTBATCHINFO c,member.member_info d WHERE a.C_FUNDCODE = b.C_FUNDCODE and  a.C_FUNDCODE = c.C_FUNDCODE and c.c_trustee = d.mem_code and a.C_FUNDCODE = '000L7Y';


--第二步：不是分级产品，执行下面的逻辑
--TPDTBASICINFO C_PRDREGNO 登记编码
-- d_accessstoredate 登记时间
--TPDTBATCHINFO F_BATCHFACTPAYBALA 发行规模（实际缴款规模）  单位是元
--TPDTBATCHINFO C_TRUSTEE 产品托管人
select a.C_PRDREGNO,TO_CHAR (b.d_accessstoredate,'yyyy-mm-dd') as d_accessstoredate,c.F_BATCHFACTPAYBALA,
 d.mem_name
FROM tfundinfo o,TPDTBASICINFO a ,TPDTOPERATEINFO b,TPDTBATCHINFO c,member.member_info d WHERE o.c_fundcode = a.c_fundcode and a.C_FUNDCODE = b.C_FUNDCODE and  a.C_FUNDCODE = c.C_FUNDCODE and c.c_trustee = d.mem_code and o.c_tafundcode = '10924000070';


--不管是否是分期产品，储架规模的查询逻辑都是一样的。
--储架规模

SELECT * FROM (SELECT a.F_PRDREGBALA FROM fundcrm.TPDTBASICINFO a ,fundcrm.TPDTOPERATEINFO b 
WHERE a.C_FUNDCODE = b.C_FUNDCODE and A.C_PRDREGNO = 'ZC2024070038' ORDER BY b.d_accessstoredate ASC ) WHERE ROWNUM = 1;