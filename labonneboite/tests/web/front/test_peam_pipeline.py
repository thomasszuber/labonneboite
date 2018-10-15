from social_flask.utils import load_strategy

from labonneboite.web.auth.backends import peam
from labonneboite.tests.test_base import DatabaseTest


class AuthPipelineTest(DatabaseTest):

    def run_pipeline(self, BackendClass):
        with self.test_request_context:
            strategy = load_strategy()
            backend = BackendClass(strategy=strategy)
            pipeline = strategy.get_pipeline(backend)
            result = backend.run_pipeline(
                pipeline, pipeline_index=0,
                backend=backend,
                is_new=False,
                response={
                    'access_token': 'access-token',
                    'email': 'my@email.com',
                    'expires_in': 1000,
                    'given_name': 'ELTON',
                    'family_name': 'JOHN',
                    'gender': 'male',
                    'id_token': 'loooooooongstring',
                    'nonce': 'longnonce',
                    'refresh_token': 'refresh-token',
                    'scope': 'application_PAR_lbb_scope email api_peconnect-individuv1 openid profile',
                    'sub': 'peconnect-userid',
                    'token_type': 'Bearer',
                    'updated_at': '0'
                },
                storage=strategy.storage,
                strategy=strategy,
                user=None
            )
            return result

    def test_run_pipeline_with_PEAMOpenIdConnect(self):
        result = self.run_pipeline(peam.PEAMOpenIdConnect)
        self.assertIn('user', result)

    def test_run_pipeline_with_PEAMOpenIdConnectNoPrompt(self):
        result = self.run_pipeline(peam.PEAMOpenIdConnectNoPrompt)
        self.assertIn('user', result)

    def test_run_pipeline_twice(self):
        result1 = self.run_pipeline(peam.PEAMOpenIdConnect)
        result2 = self.run_pipeline(peam.PEAMOpenIdConnectNoPrompt)
        self.assertEqual(result1['user'].id, result2['user'].id)