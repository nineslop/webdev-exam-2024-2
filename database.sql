-- MySQL dump 10.13  Distrib 8.0.33, for Linux (x86_64)
--
-- Host: std-mysql    Database: std_2435_exam
-- ------------------------------------------------------
-- Server version	5.7.26-0ubuntu0.16.04.1

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('43175a336131');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `year` int(11) NOT NULL,
  `publisher` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `pages` int(11) NOT NULL,
  `cover_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_books_cover_id_covers` (`cover_id`),
  CONSTRAINT `fk_books_cover_id_covers` FOREIGN KEY (`cover_id`) REFERENCES `covers` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=61 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (39,'Женщина в белом','Жизнь начинающего художника Уолтера Хартрайта, получившего в уединенном имении необременительную должность учителя рисования, навеки изменилась после встречи с таинственной молодой незнакомкой, одетой в белое…\nКто она? Почему так отчаянно проклинает какого-то баронета? Что за всадники скачут по ее следу? И наконец, почему она похожа на одну из учениц Уолтера, словно сестра-близнец? Решив выяснить это, художник, сам того не подозревая, оказывается впутан в загадочную историю, полную тщательно хранимых годами фамильных секретов. Секретов, опасных для всех - и прежде всего для того, кто попытается их раскрыть…',2022,'АСТ','Коллинз Уилки',768,23),(40,'Игра престолов. Книга 1','Литературная основа популярного сериала \"Игра престолов\"\nПервая книга культового цикла \"Песнь льда и пламени\", главного фэнтези-цикла последних 20 лет\nПеред вами - величественное шестикнижие \"Песнь льда и пламени\". Эпическая, чеканная сага о мире Семи Королевств. О мире суровых земель вечного холода и радостных земель вечного лета. Мире лордов и героев, воинов и магов, чернокнижников и убийц - всех, кого свела воедино Судьба во исполнение древнего пророчества. О мире опасных приключений, великих деяний и тончайших политических интриг.',2023,'АСТ','Мартин Джордж Р. Р.',768,24),(42,'Гроздья гнева','\"В душах людей наливаются и зреют Гроздья гнева - тяжелые гроздья, и дозревать им теперь уже недолго...\" Культовый роман Джона Стейнбека \"Гроздья гнева\" впервые был опубликован в Америке в 1939 году, получил Пулицеровскую премию, а сам автор позднее был награжден Нобелевской премией по литературе. На сегодняшний день \"Гроздья гнева\" входят во многие учебные программы школ и колледжей США.\nВо время Великой депрессии семья разоренных фермеров вынуждена покинуть свой дом в Оклахоме. По знаменитой \"Road 66\" через всю Америку, как и миллионы других безработных, они едут, идут и даже ползут на запад, в вожделенную Калифорнию. Но что их там ждет? И есть ли хоть какая-то надежда на светлое будущее?',2023,'Азбука','Стейнбек Джон',608,25),(43,'Автостопом по Галактике. Ресторан \"У конца Вселенной\"','\"Автостопом по галактике\", стартовав в качестве радиопостановки на Би-би-си, имел грандиозный успех. Одноименный роман в 1984 году возглавил список английских бестселлеров, а сам Адамс стал самым молодым писателем, получившим награду \"Золотая ручка\", вручаемую за 1 млн. проданных книг.\nТелепостановка 1982 года упрочила успех серии книг про \"Автостоп\", а полнометражный фильм 2005 года при бюджете в $50 млн. дважды \"отбил\" расходы на экранизацию и был номинирован на 7 премий.\nПопулярность сатирической \"трилогии в пяти частях\" выплеснулась в музыкальную и компьютерную индустрию. Так, группы Radiohead, Coldplay, NOFX используют цитаты из романа Адамса, а Level 42 названа в честь главной сюжетной линии романа.\nГерои не менее культового фильма \"Люди в черном\" беззастенчиво пользуются саркастическими диалогами персонажей Адамса.',2022,'АСТ','Адамс Дуглас',320,26),(44,'451 градус по Фаренгейту','451° по Фаренгейту - температура, при которой воспламеняется и горит бумага. Философская антиутопия Брэдбери рисует беспросветную картину развития постиндустриального общества: это мир будущего, в котором все письменные издания безжалостно уничтожаются специальным отрядом пожарных, а хранение книг преследуется по закону, интерактивное телевидение успешно служит всеобщему оболваниванию, карательная психиатрия решительно разбирается с редкими инакомыслящими, а на охоту за неисправимыми диссидентами выходит электрический пес…\nРоман, принесший своему творцу мировую известность.',2023,'Эксмо-Пресс','Брэдбери Рэй',256,27),(45,'Властелин Колец. Братство кольца','\"Властелин Колец: Братство Кольца\" - проект ХХI века. Голливудское чудо произросшее по воле одного из самых оригинальных режиссеров современности Питера Джексона, у него на родине в Новой Зеландии. Картина была названа лучшим фильмом года и получила четыре \"Оскара\": за операторскую работу, грим, спецэффекты и музыку, а гильдия режиссеров Америки признала Питера Джексона лучшим режиссером года. Поистине волшебной была игра таких звезд как Элайа Вуд, Кристофер Ли, Лив Тайлер и Кейт Бланшетт.\nЕдиное Кольцо, связующее народы Средиземья в гармоничное и прекрасное целое - вожделенная цель о которой мечтает Темный Властелин, которому подвластны лишь силы мрака и зла, несущие смерть и хаос. Братство Кольца призвано беречь его Хранителя, маленького, но мужественного хоббита Фродо, выбранного для уничтожения ставшей опасной святыни.',2003,'Центрполиграф','Толкин Джон Рональд Руэл',542,28),(46,'Стивен Кинг: Сияние','Культовый роман Стивена Кинга.\nРоман, который и сейчас, спустя тридцать с лишним лет после триумфального выхода в свет, читается так, словно был написан вчера.\nКнига, вновь и вновь издающаяся едва ли не на всех языках мира.\nПеред вами - одно из лучших произведений Мастера в новом переводе!\n…Проходят годы, десятилетия, но потрясающая история писателя Джека Торранса, его сынишки Дэнни, наделенного необычным даром, и поединка с темными силами, обитающими в роскошном отеле \"Оверлук\", по-прежнему завораживает и держит в неослабевающем напряжении читателей самого разного возраста…\nКакое же бесстрашное воображение должно быть у писателя, создавшего подобную книгу!\n\"The Observer\"\nО странном и пугающем Стивену Кингу, пожалуй, известно не меньше, чем самому Эдгару По.\nEntertainment Weekly\nКинг не просто пугает, - он делает это мастерски и талантливо!\nLos Angeles Times\nКинг не имеет себе равных в истории литературы ужасов.\nThe Washington Post',2014,'АСТ','Кинг Стивен',544,29),(47,'Молчание ягнят','Мы все безумцы или, может быть, это мир вокруг нас сошел с ума?\nДоктор Ганнибал Лектер - блестящий психиатр, но мир может считать себя в безопасности только до тех пор, пока он будет находиться за стальной дверью одиночной камеры в тюрьме строгого режима. Доктор Лектер - убийца. Он гурман-людоед. Клэрис Стерлинг - курсант академии ФБР. Она восприимчива к чужой беде, и именно это определяет все ее поступки.\nСудьба заставляет героев действовать совместно в деле о поимке Буффало Билла - опаснейшего маньяка-убийцы.\nСенсационная экранизация романа \"Молчание ягнят\" получила пять премий \"Оскар\".',2012,'Эксмо-Пресс','Харрис Томас Энтони',512,30),(51,'ИИ-2041. Десять образов нашего будущего','Искусственный интеллект станет определяющим событием XXI века. В течение двух десятилетий все аспекты повседневной жизни станут неузнаваемыми. ИИ приведет к беспрецедентному богатству, симбиоз человека и машины приведет к революции в медицине и образовании и создаст совершенно новые формы общения и развлечений. Однако, освобождая нас от рутинной работы, ИИ также бросит вызов организационным принципам нашего экономического и социального порядка. ИИ принесет новые риски в виде автономного оружия и неоднозначных интеллектуальных технологий. ИИ находится в переломном моменте, и людям необходимо узнать как его положительные черты ИИ, так и экзистенциальные опасности, которые он может принести.\n\nВ этой провокационной, совершенно оригинальной работе Кай-Фу Ли, бывший президент Google China и автор книги «Сверхдержавы искусственного интеллекта», объединяется со знаменитым романистом Чэнь Цюфанем, чтобы представить наш мир в 2041 году и то, как он будет формироваться с помощью ИИ. В...',2022,'Манн, Иванов и Фербер','Ли Кай-Фe',432,31),(52,'Клуб самоубийц','Добро пожаловать в мир удивительных приключений и хитро задуманных преступлений, головокружительных погонь, смертельных дуэлей и умопомрачительно смешных диалогов, - мир, в котором викторианский \"рыцарь без страха и упрека\" принц Флоризель и его верный друг полковник Джеральдин ведут смертельную схватку со Злом, защищая несправедливо обиженных, - и ни на минуту не теряют при этом достойного истинных джентльменов чувства юмора.',2021,'АСТ','Роберт Стивенсон',256,32);
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books_genres`
--

DROP TABLE IF EXISTS `books_genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books_genres` (
  `book_id` int(11) NOT NULL,
  `genre_id` int(11) NOT NULL,
  PRIMARY KEY (`book_id`,`genre_id`),
  KEY `fk_books_genres_genre_id_genres` (`genre_id`),
  CONSTRAINT `fk_books_genres_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_books_genres_genre_id_genres` FOREIGN KEY (`genre_id`) REFERENCES `genres` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books_genres`
--

LOCK TABLES `books_genres` WRITE;
/*!40000 ALTER TABLE `books_genres` DISABLE KEYS */;
INSERT INTO `books_genres` VALUES (43,1),(44,1),(39,2),(52,3),(40,4),(45,4),(47,5),(52,5),(43,6),(42,7),(52,7),(46,8),(40,9),(43,9),(45,9),(51,10);
/*!40000 ALTER TABLE `books_genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `covers`
--

DROP TABLE IF EXISTS `covers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `covers` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `filename` varchar(255) NOT NULL,
  `mime_type` varchar(255) NOT NULL,
  `md5_hash` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `covers`
--

LOCK TABLES `covers` WRITE;
/*!40000 ALTER TABLE `covers` DISABLE KEYS */;
INSERT INTO `covers` VALUES (12,'AHHAAHA.png','image/png','09ab4b169c3d85bfc13e28009c048c57'),(23,'womb.jpg','image/jpeg','06eca2a7c1c136cde34cae8c3a2e0da0'),(24,'igra.png','image/png','c7026aed009353811f382bf6b328b978'),(25,'grozdia.jpg','image/jpeg','a7015b0efadf110b843d03508df29864'),(26,'galaxy.jpg','image/jpeg','f5427ca1c509c6d2c6ec47933fa76c20'),(27,'451.jpg','image/jpeg','c15d81f883a15b9d9b5cb049c5a00dee'),(28,'ring.jpg','image/jpeg','36e04d7821f4dd3f33df5dbecbc791b6'),(29,'sijanie.jpg','image/jpeg','36daf559f3c9f1546def6faf2ea79bb4'),(30,'silence.jpg','image/jpeg','f4f096796965074c1e29fb0bcc66b33e'),(31,'Intele.jpg','image/jpeg','dc171b363128baad1c8e5f4bfa2afce7'),(32,'clubkiller.jpg','image/jpeg','9fa4cc5e4aa68811f75c74ef66383b0e');
/*!40000 ALTER TABLE `covers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `genres`
--

DROP TABLE IF EXISTS `genres`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `genres` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_genres_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `genres`
--

LOCK TABLES `genres` WRITE;
/*!40000 ALTER TABLE `genres` DISABLE KEYS */;
INSERT INTO `genres` VALUES (3,'Детектив'),(7,'Драма'),(6,'Комедия'),(10,'Научно-популярное'),(9,'Приключения'),(2,'Роман'),(5,'Триллер'),(8,'Ужасы'),(1,'Фантастика'),(4,'Фэнтези');
/*!40000 ALTER TABLE `genres` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reviews`
--

DROP TABLE IF EXISTS `reviews`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reviews` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `book_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `rating` int(11) NOT NULL,
  `text` text NOT NULL,
  `date_added` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `fk_reviews_book_id_books` (`book_id`),
  KEY `fk_reviews_user_id_users` (`user_id`),
  CONSTRAINT `fk_reviews_book_id_books` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE,
  CONSTRAINT `fk_reviews_user_id_users` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reviews`
--

LOCK TABLES `reviews` WRITE;
/*!40000 ALTER TABLE `reviews` DISABLE KEYS */;
INSERT INTO `reviews` VALUES (5,42,1,4,'Крутая!!!','2024-06-14 15:38:17'),(6,40,2,0,'Книга разочаровала((((((','2024-06-14 15:54:55'),(7,42,2,3,'Нормальная книга','2024-06-14 15:56:06'),(8,44,2,5,'Роман поучителен, захватывает с первых страниц. Самое главное я думаю здесь то, что затронута главная проблема общества-деградация. В наше время серф по тик-току и инстаграм-это наиболее увлекательное времяпровождение. Роман о важности книг в нашем мире, об их силе и пользе. Люди действительно не хотят задумываться о важных вещах, у них нет ценностей. Живут с девизом-«мне все равно». Будь моя воля, я бы добавила эту книгу в школьную программу, читается несложно и сколько смысла заложено!','2024-06-14 15:56:37'),(9,39,2,1,'\"Женщина в белом\" Уилки Коллинза - это, без сомнения, одна из самых переоцененных книг, которые мне доводилось читать. С самого начала меня поразила затянутость и медлительность сюжета. Описания бесконечных прогулок и разговоров героев растягиваются на страницы, не добавляя никакого реального развития или интереса к истории.','2024-06-14 16:00:31'),(10,51,2,5,'\"ИИ-2041. Десять образов нашего будущего\" — это захватывающий и глубокий взгляд на будущее, написанный дуэтом экспертов Кай-Фу Ли и Чена Цюфаня. Книга предлагает уникальное сочетание научно-фантастических рассказов и аналитических эссе, что делает ее не только увлекательной, но и поучительной.','2024-06-14 16:01:25'),(11,40,1,5,'\"Игра престолов\" Джорджа Р.Р. Мартина - это великолепное начало эпической саги \"Песнь Льда и Огня\", которое сразу же захватывает читателя и погружает в богатый, детально проработанный мир Вестероса. Мартин мастерски сочетает элементы фэнтези, политики, интриг и драмы, создавая уникальный и незабываемый роман.','2024-06-14 16:02:42'),(12,44,1,4,'\"451 градус по Фаренгейту\" — это произведение, которое оставляет неизгладимый след в сердце каждого, кто обратил внимание на светлую искру истины, проникающую сквозь покрывало тьмы, наложенное на наше общество. Рэй Брэдбери, создатель этого мастерского произведения, нарисовал перед нами мрачный образ будущего, где книги запрещены и горят в пожарах, разжигаемых самими пожарными, воплощая образ книги-пророчества.','2024-06-14 16:03:31'),(13,40,3,3,'Норм','2024-06-14 16:04:17'),(14,42,3,1,'Ну такое если честно','2024-06-14 16:04:52'),(15,44,3,1,'Не моё','2024-06-14 16:05:43'),(16,39,3,5,'Очень интересная книга, очень понравилась','2024-06-14 16:06:07'),(17,51,1,4,'&lt;script&gt;alert(\'XSS\');&lt;/script&gt;','2024-06-14 16:45:09');
/*!40000 ALTER TABLE `reviews` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `roles`
--

DROP TABLE IF EXISTS `roles`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `roles` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `description` text NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `roles`
--

LOCK TABLES `roles` WRITE;
/*!40000 ALTER TABLE `roles` DISABLE KEYS */;
INSERT INTO `roles` VALUES (1,'администратор','суперпользователь, имеет полный доступ к системе, в том числе к созданию и удалению книг'),(2,'модератор','может редактировать данные книг и производить модерацию рецензий'),(3,'пользователь','может оставлять рецензии');
/*!40000 ALTER TABLE `roles` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `login` varchar(255) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `middle_name` varchar(255) NOT NULL,
  `role_id` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `uq_users_login` (`login`),
  KEY `fk_users_role_id_roles` (`role_id`),
  CONSTRAINT `fk_users_role_id_roles` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Admin','scrypt:32768:8:1$ch6f8WAscSEB0Gih$f7e18333f9d381e8bab13bae7c4b8479bca274df7751b392b5e438702493e6801c0c0ccfa0f205ca6f0d6882eff392fc84bae8d042594772d131751b833c016e','Иванов','Владислав','',1),(2,'moderator','scrypt:32768:8:1$Dc1YosdTUZfhPFtV$a42d5137256e0cc90f68552af7b85a7071624c4fb780f6510bf1de835d53a933d0ac8926888e06dc6c52c52b84caff28ca5890feeea7e8a79b452cb38414dc56','Савинкин','Илья','',2),(3,'user','scrypt:32768:8:1$EV6Vt2yM0kjaSjd1$5910986e3942200e2ed8058dc4b640470aafe62c06645b921171ac1c84b561bc772c7d8d06c60eb852047c5d2abbd79c26b11ee5b7080d7fef73f02b0ee33a02','Гуржам','Хачапури','',3);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-06-14 16:51:59
