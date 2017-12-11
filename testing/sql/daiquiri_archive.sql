DROP DATABASE IF EXISTS `daiquiri_archive`;
CREATE DATABASE `daiquiri_archive`;

USE `daiquiri_archive`;


CREATE TABLE IF NOT EXISTS `files` (
    `id`          CHAR(36) PRIMARY KEY NOT NULL,
    `timestamp`   DATETIME NOT NULL,
    `file`        VARCHAR(256) NOT NULL,
    `collection`  CHAR(32) NOT NULL,
    `path`        TEXT NOT NULL,
    `ra`          FLOAT NOT NULL,
    `de`          FLOAT NOT NULL
) ENGINE=Aria;

LOCK TABLES `files` WRITE;
INSERT INTO `files` VALUES ('396d75e1-7dc6-4028-a5c1-25b6cfc007ff', '2017-10-01 00:00:00', 'image_00', 'c00', 'images/image_00.jpg', 70.88628666205052, -19.979442951664748), ('040926e2-51ac-4ce1-be2e-7f8deb10ea06', '2017-10-02 00:00:00', 'image_01', 'c01', 'images/image_01.jpg', 78.06483743765392, -38.23549628575872), ('6b915269-5b47-4d6e-9020-1e0996df21ae', '2017-10-03 00:00:00', 'image_02', 'c02', 'images/image_02.jpg', 89.09620093217619, 36.522791691329545), ('0c1ce06b-4eff-4891-96e6-e383564209c2', '2017-10-04 00:00:00', 'image_03', 'c03', 'images/image_03.jpg', 87.47321485852328, -10.55908737183129), ('290e1654-af85-429a-8872-d235b54652f0', '2017-10-05 00:00:00', 'image_04', 'c04', 'images/image_04.jpg', -41.88919163492463, 36.685755976479996), ('b2524e51-6bfa-404f-8f61-ea4962737167', '2017-10-06 00:00:00', 'image_05', 'c05', 'images/image_05.jpg', -0.02526628767763217, 43.30281747422392), ('c319d5ac-894b-479c-b447-225e4afe86ed', '2017-10-07 00:00:00', 'image_06', 'c06', 'images/image_06.jpg', 72.16707584866379, 4.674128454786462), ('26941dc2-5572-4ee3-b144-83203437d63a', '2017-10-08 00:00:00', 'image_07', 'c07', 'images/image_07.jpg', -24.52637471539052, -4.295124536064331), ('d5da83d7-cc8e-4e54-bdb1-27af107719c3', '2017-10-09 00:00:00', 'image_08', 'c08', 'images/image_08.jpg', 60.32160623810525, -34.65704373667677), ('bb0bac5b-75ca-4ff4-842f-38a4a93546b3', '2017-10-10 00:00:00', 'image_09', 'c09', 'images/image_09.jpg', -9.00783452294694, -31.12615618822415), ('61238427-a165-48bd-8a52-3c186119509c', '2017-10-11 00:00:00', 'image_10', 'c10', 'images/image_10.jpg', -59.3294453468344, -34.2863566226582), ('ab3be662-8426-4120-aa68-bfcd35c7bf32', '2017-10-12 00:00:00', 'image_11', 'c11', 'images/image_11.jpg', 83.90300419177264, -29.259864568753944), ('6b6fda7c-666e-49cf-9a66-965926666e3c', '2017-10-13 00:00:00', 'image_12', 'c12', 'images/image_12.jpg', 26.58869096462412, 44.62002965264193), ('7c67abb6-6d3f-46af-89b9-059e86d4621d', '2017-10-14 00:00:00', 'image_13', 'c13', 'images/image_13.jpg', -47.413530328036686, -21.389039977891912), ('70d9328d-067c-40a9-86e5-3068a608241c', '2017-10-15 00:00:00', 'image_14', 'c14', 'images/image_14.jpg', 74.55804785188367, 10.868377358833936), ('522eada2-ea2a-4c7a-a093-6f2fc8279743', '2017-10-16 00:00:00', 'image_15', 'c15', 'images/image_15.jpg', 40.47804047468472, -29.35522603509017), ('a9ba43f5-b4ed-4ad0-92ea-bfa42e92028f', '2017-10-17 00:00:00', 'image_16', 'c16', 'images/image_16.jpg', 32.75238081919178, 15.360589441740514), ('34d8d0b5-c0e9-4305-ad50-2c8087c2e337', '2017-10-18 00:00:00', 'image_17', 'c17', 'images/image_17.jpg', 62.163616173293995, 10.559417365484512), ('82163604-c5dd-4059-a7d9-9a4c9d97a999', '2017-10-19 00:00:00', 'image_18', 'c18', 'images/image_18.jpg', 52.23625788695439, -23.73168061640149), ('89728541-aa8f-448c-8d10-62deed956f49', '2017-10-20 00:00:00', 'image_19', 'c19', 'images/image_19.jpg', -72.6978935341401, -38.62642795804832), ('7254b8ee-d94d-4dd9-82b6-5c630900a252', '2017-10-01 00:00:00', 'image_00', 'c00', 'images/image_00.fits', -34.9551371622724, -39.8348059360132), ('b0d25268-2194-40c3-9a3a-ba987d21725f', '2017-10-02 00:00:00', 'image_01', 'c01', 'images/image_01.fits', -52.51585009952077, -9.075221284785036), ('df0b439d-40ac-41a9-b78e-b6e3f6ab37d4', '2017-10-03 00:00:00', 'image_02', 'c02', 'images/image_02.fits', -13.312657399423838, 29.997252944343305), ('e164c2be-cb0a-4f62-9d0a-3a68dc17203b', '2017-10-04 00:00:00', 'image_03', 'c03', 'images/image_03.fits', -20.16735032241918, 0.19379442708112427), ('0013f37c-a6f6-4f8d-9cd2-7808ae6ad6d5', '2017-10-05 00:00:00', 'image_04', 'c04', 'images/image_04.fits', -86.007170846007, 22.471157888128083), ('3010c60c-0900-40f1-9f55-2bd15b99fa39', '2017-10-06 00:00:00', 'image_05', 'c05', 'images/image_05.fits', 71.19316264030248, 37.74387991995621), ('ba4553df-a5df-4512-b887-77d85c511e91', '2017-10-07 00:00:00', 'image_06', 'c06', 'images/image_06.fits', -71.0561766344956, -44.158847306917615), ('76dce365-bf17-4b09-b7cd-3f0b37c51ea2', '2017-10-08 00:00:00', 'image_07', 'c07', 'images/image_07.fits', -40.89581991605861, 2.7528309808162312), ('058d81ee-313e-4471-9ee6-dc61815aa3ae', '2017-10-09 00:00:00', 'image_08', 'c08', 'images/image_08.fits', -40.43861868958945, -43.593985519118156), ('3b4d64f5-86fe-447c-89b1-590248421cd2', '2017-10-10 00:00:00', 'image_09', 'c09', 'images/image_09.fits', 88.95412991284212, -30.656551255746095), ('46c7d5fc-55b4-49d7-bc50-ef46f0c6ec32', '2017-10-11 00:00:00', 'image_10', 'c10', 'images/image_10.fits', 14.484803955396758, 16.835547974845667), ('6675e150-c29b-4cda-8b09-2326efe723db', '2017-10-12 00:00:00', 'image_11', 'c11', 'images/image_11.fits', 4.805028300944112, -32.31752327751441), ('49a4f8a3-9a23-466a-b049-e669a4234f89', '2017-10-13 00:00:00', 'image_12', 'c12', 'images/image_12.fits', 54.3506864002025, -16.0956191510574), ('1828070f-561c-47e9-8ee0-af332d7deed9', '2017-10-14 00:00:00', 'image_13', 'c13', 'images/image_13.fits', 4.679610976423851, 43.581457323898405), ('64206cc6-5bcf-444d-ad5e-b0c62618c42b', '2017-10-15 00:00:00', 'image_14', 'c14', 'images/image_14.fits', 80.05429640042665, 5.391939507409836), ('86aab01f-a0de-415a-b00a-ed8454e1dd2c', '2017-10-16 00:00:00', 'image_15', 'c15', 'images/image_15.fits', 73.56856393140298, 36.26060764072612), ('dbf5f828-5160-4061-a2dd-28d5ba0c7d3c', '2017-10-17 00:00:00', 'image_16', 'c16', 'images/image_16.fits', 85.59006586500354, 39.998030663937875), ('0c4d6411-7d77-4b5e-b9ca-e967cf46702b', '2017-10-18 00:00:00', 'image_17', 'c17', 'images/image_17.fits', 9.618087123441882, 41.09272740582363), ('24b36074-da87-4177-ac7c-e915a5860034', '2017-10-19 00:00:00', 'image_18', 'c18', 'images/image_18.fits', -77.7689955099905, 25.13402042027589), ('ae099704-5d1a-4d18-bbd4-5c71f8a63edf', '2017-10-20 00:00:00', 'image_19', 'c19', 'images/image_19.fits', 48.495407141656, 44.23576081181626);

UNLOCK TABLES;
