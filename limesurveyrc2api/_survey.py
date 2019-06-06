import warnings
from collections import OrderedDict
from limesurveyrc2api.exceptions import LimeSurveyError
from os.path import splitext
from base64 import b64encode


class _Survey(object):
    def __init__(self, api):
        self.api = api

    def list_surveys(self, username=None):
        """
        List surveys accessible to the specified username.

        Parameters
        :param username: LimeSurvey username to list accessible surveys for.
        :type username: String
        """
        method = "list_surveys"
        params = OrderedDict([("sSessionKey", self.api.session_key),
                              ("iSurveyID", username or self.api.username)])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Invalid user", "No surveys found", "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response

    def list_questions(self, survey_id, group_id=None, language=None):
        """
        Return a list of questions from the specified survey.

        Parameters
        :param survey_id: ID of survey to list questions from.
        :type survey_id: Integer
        :param group_id: ID of the question group to filter on.
        :type group_id: Integer
        :param language: Language of survey to return for.
        :type language: String
        """
        method = "list_questions"
        params = OrderedDict([("sSessionKey",
                               self.api.session_key), ("iSurveyID", survey_id),
                              ("iGroupID", group_id), ("sLanguage", language)])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID", "Error: Invalid language",
                "Error: IMissmatch in surveyid and groupid",
                "No questions found", "No permission", "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response

    def import_question(self, survey_id, group_id, import_data,
                        import_data_type, mandatory_option, question_title,
                        question_text, question_help_text):
        """
        Import a question from lsq file.

        Parameters
        :param survey_id: The ID of the Survey that the question will belong to.
        :type survey_id: Integer
        :param group_id: The ID of the Group that the question will belong to.
        :type group_id: Integer
        :param import_data: String containing the BASE 64 encoded data of a lsq.
        :type import_data: String
        :param import_data_type: lsq.
        :type import_data_type: String
        :param mandatory_option: Mandatory question option (default to No).
        :type mandatory_option: String
        :param question_title: new title for the question.
        :type question_title: String
        :param question_text: new question text.
        :type question_text: String
        :param question_help_text: new question help text.
        :type question_help_text: String
        """
        method = "import_question"
        params = OrderedDict(
            [("sSessionKey", self.api.session_key), ("iSurveyID", survey_id),
             ("iGroupID", group_id), ("sImportData", import_data),
             ("sImportDataType", import_data_type), ("sMandatory",
                                                     mandatory_option),
             ("sNewQuestionTitle",
              question_title), ("sNewqQuestion",
                                question_text), ("sNewQuestionHelp",
                                                 question_help_text)])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "Error: IMissmatch in surveyid and groupid", "No permission",
                "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is int
        return response

    def add_survey(self, desired_survey_id, survey_title,
                   default_survey_language, appearance_format):
        """ Add an empty survey with minimum details.
        
        Parameters
        :param desired_survey_id: The desired ID of the Survey to add.
        :type desired_survey_id: Integer
        :param survey_title: Title of the new Survey.
        :type survey_title: String
        :param default_survey_language: Default language of the Survey.
        :type default_survey_language: String
        :param appearance_format: (optional) Question appearance format 
                                  (A, G or S) for "All on one page", 
                                  "Group by Group", "Single questions", 
                                  default to group by group (G).
        :type appearance_format: String
        
        """
        method = "add_survey"
        params = OrderedDict(
            [("sSessionKey", self.api.session_key),
             ("iSurveyID", desired_survey_id), ("sSurveyTitle ", survey_title),
             ("sSurveyLanguage  ",
              default_survey_language), ("sformat  ", appearance_format)])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "No permission", "Invalid session key", "Faulty parameters",
                "Creation Failed result"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is int
        return response

    def delete_survey(self, survey_id):
        """ Delete a survey.
        
        Parameters
        :param survey_id: The ID of the Survey to be deleted.
        :type: Integer
        """
        method = "delete_survey"
        params = OrderedDict([("sSessionKey", self.api.session_key),
                              ("iSurveyID", survey_id)])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = ["No permission", "Invalid session key"]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response

    def export_responses(self,
                         survey_id,
                         document_type,
                         language_code=None,
                         completion_status='all',
                         heading_type='code',
                         response_type='short',
                         from_response_id=None,
                         to_response_id=None,
                         fields=None):
        """ Export responses in base64 encoded string.
        
        Parameters
        :param survey_id: Id of the Survey.
        :type survey_id: Integer
        :param document_type: Any format available by plugins 
                             (e.g. pdf, csv, xls, doc, json)
        :type document_type: String
        :param language_code: (optional) The language to be used.
        :type language_code: String
        :param completion_status: (optional) 'complete', 'incomplete' or 'all'
        :type completion_status: String
        :param heading_type: (optional) 'code', 'full' or 'abbreviated'
        :type heading_type: String
        :param response_type: (optional) 'short' or 'long'
        :type response_type: String
        :param from_response_id: (optional)
        :type from_response_id: Integer
        :param to_response_id: (optional)
        :type to_response_id: Integer
        :param fields: (optional) Selected fields.
        :type fields: Array
        """
        method = "export_responses"
        params = OrderedDict(
            [("sSessionKey", self.api.session_key), ("iSurveyID", survey_id),
             ("sDocumentType",
              document_type), ("sLanguageCode",
                               language_code), ("sCompletionStatus",
                                                completion_status),
             ("sHeadingType", heading_type), ("sResponseType", response_type),
             ("iFromResponseID",
              from_response_id), ("iToResponseID", to_response_id), ("aFields",
                                                                     fields)])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Language code not found for this survey.",
                "No Data, could not get max id.",
                "No Data, survey table does not exist", "No permission",
                "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is str
        return response

    def get_question_properties(self,
                                question_id,
                                question_setting='all',
                                language_code=None):
        """ Get properties of a question in a survey.
        
        Parameters
        :param question_id: ID of the question to get properties.
        :type question_id: Integer
        :param question_setting: (optional) properties to get, default to all.
        :type question_setting: Array
        :param language_code: (optional) parameter language for multilingual
                              questions, default are \Survey->language.
        :type language_code: String
        """
        method = "get_question_properties"
        params = OrderedDict([("sSessionKey", self.api.session_key),
                              ("iQuestionID", question_id),
                              ("aQuestionSettings",
                               question_setting), ("sLanguage",
                                                   language_code)])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = ["No permission", "Invalid session key"]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response

    def import_survey(self,
                      path_to_import_survey,
                      new_name=None,
                      dest_survey_id=None):
        """ Import a survey. Allowed formats: lss, csv, txt or lsa

        Parameters
        :param path_to_import_survey: Path to survey as file to copy.
        :type path_to_import_survey: String
        :param new_name: (optional) The optional new name of the survey
                    Important! Seems only to work if lss file is given!
        :type new_name: String
        :param dest_survey_id: (optional) This is the new ID of the survey - 
                          if already used a random one will be taken instead
        :type dest_survey_id: Integer
        """
        import_datatype = splitext(path_to_import_survey)[1][1:]
        # TODO: Naming seems only to work with lss files - why?
        if import_datatype != 'lss' and new_name:
            warnings.warn("New naming seems only to work with lss files",
                          RuntimeWarning)
        # encode import data
        with open(path_to_import_survey, 'rb') as f:
            # import data must be a base 64 encoded string
            import_data = b64encode(f.read())
            # decoding needed because json.dumps() in method get of
            # class LimeSurvey can not encode bytes
            import_data = import_data.decode('ascii')

        method = "import_survey"
        params = OrderedDict([("sSessionKey", self.api.session_key),
                              ("sImportData", import_data), ("sImportDataType",
                                                             import_datatype),
                              ("sNewSurveyName", new_name), ("DestSurveyID",
                                                             dest_survey_id)])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: ...",  # TODO: Unclear what might be returned here
                "Invalid extension",
                "No permission",
                "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is int  # the new survey id
        return response

    def activate_survey(self, survey_id):
        """ Activate an existing survey.
        
        Parameters
        :param survey_id: Id of the Survey to be activated.
        :type survey_id: Integer
        """
        method = "activate_survey"
        params = OrderedDict([("sSessionKey", self.api.session_key),
                              ("iSurveyID", survey_id)])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "Error: ...",  # TODO: what could be output of ActivateResults?
                "No permission",
                "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response

    def activate_tokens(self, survey_id, attribute_fields=[]):
        """
        
        Parameters
        :param survey_id: ID of the Survey where a participants table will
            be created for.
        :type survey_id: Integer
        :param attribute_fields: An array of integer describing any additional 
            attribute fiields.
        :type attribute_fields: Array
        """
        method = "activate_tokens"
        params = OrderedDict([("sSessionKey", self.api.session_key),
                              ("iSurveyId", survey_id), ("aAttributeFields",
                                                         attribute_fields)])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "Survey participants table could not be created",
                "No permission", "Invalid session key"
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response

    def list_groups(self, survey_id):
        """ Return the ids and all attributes of groups belonging to survey.
        
        Parameters
        :param survey_id: ID of the survey containing the groups.
        :rtype survey_id: Integer
        """
        method = "list_groups"
        params = OrderedDict([("sSessionKey", self.api.session_key),
                              ("iSurveyID", survey_id)])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "No groups found",
                "No permission"
                "Invalid S ession key"  # typo in remotecontrol_handle.php
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is list
        return response

    def add_group(self, survey_id, group_title, group_description=""):
        """ Add an empty group with minimum details to a chosen survey.
        
        Parameters
        :param survey_id: ID of the survey to add the group.
        :type survey_id: Integer
        :param group_title: Name of the group.
        :type group_title: String
        :param group_description: Optional description of the group.
        :type group_description: String
        
        """
        method = "add_group"
        params = OrderedDict(
            [("sSessionKey", self.api.session_key), ("iSurveyID", survey_id),
             ("sGroupTitle", group_title), ("sGroupDescription",
                                            group_description)])
        response = self.api.query(method=method, params=params)
        response_type = type(response)

        if response_type is dict and "status" in response:
            status = response["status"]
            error_messages = [
                "Error: Invalid survey ID",
                "No permission",
                "Invalid S ession key"  # typo in remotecontrol_handle.php
            ]
            for message in error_messages:
                if status == message:
                    raise LimeSurveyError(method, status)
        else:
            assert response_type is int
        return response
