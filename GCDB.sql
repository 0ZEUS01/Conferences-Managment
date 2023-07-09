		USE master;
		GO

		DROP DATABASE IF EXISTS GC;
		GO

		CREATE DATABASE GC;
		GO

		USE GC;
		GO

		-- Create Country table
		CREATE TABLE Country (
			country_id BIGINT IDENTITY,
			country_name NVARCHAR(MAX),
			ISO NVARCHAR(MAX),
			CONSTRAINT PK_COUNTRY PRIMARY KEY (country_id)
		);
		GO	
		-- Create Users table
		CREATE TABLE Users (
			user_id BIGINT IDENTITY,
			first_name NVARCHAR(MAX),
			last_name NVARCHAR(MAX),
			email NVARCHAR(MAX),
			phone_number NVARCHAR(MAX),
			username NVARCHAR(MAX),
			password NVARCHAR(MAX),
			birthdate DATE,
			Address NVARCHAR(MAX),
			nationality BIGINT,
			picture VARBINARY(MAX),
			isAdmin BIT DEFAULT 0,
			CONSTRAINT PK_USERS PRIMARY KEY (user_id),
			CONSTRAINT FK_COUNTRY_USERS FOREIGN KEY (nationality) REFERENCES Country(country_id)
		);
		GO


		-- Create State_conference table
		CREATE TABLE State_conference (
			state_conference_id BIGINT IDENTITY,
			state_conference_name NVARCHAR(MAX),
			CONSTRAINT PK_STATE_CONFERENCE PRIMARY KEY (state_conference_id)
		);
		GO

		-- Create organisateurs table
		CREATE TABLE Organizer (
			organizer_id BIGINT IDENTITY,
			user_id BIGINT,
			CONSTRAINT PK_ORGANIZER PRIMARY KEY (organizer_id),
			CONSTRAINT FK_USERS_ORGANIZER FOREIGN KEY (user_id) REFERENCES Users(user_id)
		);
		GO

		-- Create Conference table
		CREATE TABLE Conference (
			conference_id BIGINT IDENTITY,
			title NVARCHAR(MAX),
			country BIGINT,
			address NVARCHAR(MAX),
			start_date DATE,
			end_date DATE,
			min_participants INT,
			max_participants INT,
			state_conference_id BIGINT,
			organizer_id BIGINT,
			CONSTRAINT PK_CONFERENCE PRIMARY KEY (conference_id),
			CONSTRAINT FK_COUNTRY_CONFERENCE FOREIGN KEY (country) REFERENCES Country(country_id),
			CONSTRAINT FK_ORGANIZER_CONFERENCE FOREIGN KEY (organizer_id) REFERENCES Organizer(organizer_id),
			CONSTRAINT FK_STATE_CONFERENCE_CONFERENCE FOREIGN KEY (state_conference_id) REFERENCES State_conference(state_conference_id)
		);
		GO

		-- Create participant table
		CREATE TABLE Participant (
			participant_id BIGINT IDENTITY,
			user_id BIGINT,
			CONSTRAINT PK_PARTICIPANT PRIMARY KEY (participant_id),
			CONSTRAINT FK_USERS_PARTICIPANT FOREIGN KEY (user_id) REFERENCES Users(user_id)
		);
		GO

		-- Create participant_Conference table
		CREATE TABLE ParticipantInConference  (
			Participant_id BIGINT,
			conference_id BIGINT,
			CONSTRAINT FK_PARTICIPANT_CONFERENCE_PARTICIPANT FOREIGN KEY (Participant_id) REFERENCES Participant(Participant_id),
			CONSTRAINT FK_PARTICIPANT_CONFERENCE_CONFERENCE FOREIGN KEY (conference_id) REFERENCES Conference(conference_id),
			CONSTRAINT PK_PARTICIPANT_CONFERENCE PRIMARY KEY (Participant_id,conference_id)
		);
		GO

		-- Create searcher table
		CREATE TABLE Searcher (
			searcher_id BIGINT IDENTITY,
			user_id BIGINT,
			CONSTRAINT PK_SEARCHER PRIMARY KEY (searcher_id),
			CONSTRAINT FK_USERS_SEARCHER FOREIGN KEY (user_id) REFERENCES Users(user_id)
		);
		GO

		-- Create Articles table
		CREATE TABLE Article (
			article_id BIGINT IDENTITY,
			article_title NVARCHAR(MAX),
			article_content VARBINARY(MAX),
			article_format NVARCHAR(MAX),
			searcher_id BIGINT,
			CONSTRAINT PK_ARTICLE PRIMARY KEY (article_id),
			CONSTRAINT FK_SEARCHER_ARTICLE FOREIGN KEY (searcher_id) REFERENCES Searcher(searcher_id)
		);
		GO

		-- Create searcher table
		CREATE TABLE SearcherJoinConference (
			searcher_id BIGINT,
			conference_id BIGINT,
			article_id BIGINT,
			CONSTRAINT PK_SEARCHER_CONFERENCE PRIMARY KEY (searcher_id,conference_id),
			CONSTRAINT FK_SEARCHER_CONFERENCE_SEARCHER FOREIGN KEY (searcher_id) REFERENCES Searcher(searcher_id),
			CONSTRAINT FK_SEARCHER_CONFERENCE_CONFERENCE FOREIGN KEY (conference_id) REFERENCES Conference(conference_id),
			CONSTRAINT FK_SEARCHER_CONFERENCE_ARTICLE FOREIGN KEY (article_id) REFERENCES Article(article_id)
		);
		GO

		-- Create protractor table
		CREATE TABLE Protractor(
			protractor_id BIGINT IDENTITY,
			user_id BIGINT,
			CONSTRAINT PK_PROTRACTOR PRIMARY KEY (protractor_id),
			CONSTRAINT FK_USERS_PROTRACTOR FOREIGN KEY (user_id) REFERENCES Users(user_id)
		);
		GO

		CREATE TABLE Report (
			report_id BIGINT IDENTITY,
			report_content VARBINARY(MAX),
			report_format NVARCHAR(MAX),
			CONSTRAINT PK_REPORT PRIMARY KEY (report_id)
		);
		GO

		-- Create Protractor_Report table
		CREATE TABLE ReportWrittenBy(
			protractor_id BIGINT,
			report_id BIGINT,
			CONSTRAINT PK_PROTRACTOR_REPORT PRIMARY KEY (protractor_id,report_id),
			CONSTRAINT FK_PROTRACTOR_REPORT_PROTRACTOR FOREIGN KEY (protractor_id) REFERENCES Protractor(protractor_id),
			CONSTRAINT FK_PROTRACTOR_REPORT_REPORT FOREIGN KEY (report_id) REFERENCES Report(report_id)
		);
		GO

		-- Create Submission table
		CREATE TABLE Submission (
			submission_id BIGINT IDENTITY,
			submission_date DATE,
			conference_id BIGINT,
			article_id BIGINT,
			report_id BIGINT,
			CONSTRAINT PK_SUBMISSION PRIMARY KEY (submission_id),
			CONSTRAINT FK_CONFERENCE_SUBMISSION FOREIGN KEY (conference_id) REFERENCES Conference(conference_id),
			CONSTRAINT FK_ARTICLE_SUBMISSION FOREIGN KEY (article_id) REFERENCES Article(article_id),
			CONSTRAINT FK_REPORT_SUBMISSION FOREIGN KEY (report_id) REFERENCES Report(report_id)
		);
		GO

		-- Create Decision table
		CREATE TABLE Decision (
			decision_id BIGINT IDENTITY,
			decision NVARCHAR(MAX),
			CONSTRAINT PK_DECISION PRIMARY KEY (decision_id)
		);
		GO

		-- Create organisateurs_Submission table
		CREATE TABLE OrganizerDecision (
			organizer_id BIGINT,
			submission_id BIGINT,
			decision_id BIGINT,
			CONSTRAINT FK_ORGANIZER_ORGANIZER_SUBMISSION FOREIGN KEY (organizer_id) REFERENCES Organizer(organizer_id),
			CONSTRAINT FK_ORGANIZER_SUBMISSION_SUBMISSION FOREIGN KEY (submission_id) REFERENCES Submission(submission_id),
			CONSTRAINT PK_ORGANIZER_SUBMISSION PRIMARY KEY (organizer_id,submission_id),
			CONSTRAINT FK_DECISION FOREIGN KEY (decision_id) REFERENCES Decision(decision_id)
		);
		GO


