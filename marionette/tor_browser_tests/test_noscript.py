# https://trac.torproject.org/projects/tor/ticket/13053

from marionette_driver import By
from marionette_driver.errors import MarionetteException, NoSuchElementException

from marionette_harness import MarionetteTestCase

import testsuite
import json

class Test(MarionetteTestCase):

    def setUp(self):
        MarionetteTestCase.setUp(self)

        ts = testsuite.TestSuite()
        self.ts = ts

        self.http_url = "%s/noscript/" % ts.t['options']['test_data_url']
        self.https_url = "%s/noscript/" % ts.t['options']['test_data_url_https']


    def test_noscript(self):
        def get_iframe_csp_switch():
            iframe = self.marionette.find_element('id', 'iframe')
            self.marionette.switch_to_frame(iframe)
            csp = get_csp()
            self.marionette.switch_to_default_content()
            return csp

        def get_iframe_csp_direct():
            return json.loads(self.marionette.execute_script("return window.frames[0].content.document.nodePrincipal.cspJSON || window.frames[0].content.document.cspJSON;", sandbox="system"))

        def get_csp():
            return json.loads(self.marionette.execute_script("return document.nodePrincipal.cspJSON || document.cspJSON;", sandbox="system"))

        self.marionette.timeout.implicit = 1
        self.maxDiff = None

        with self.marionette.using_context('content'):

            # http page sourcing http js
            self.marionette.navigate("%s/http_src.html" % self.http_url)
            csp_parent = get_csp()
            print "csp parent http page sourcing http js", json.dumps(csp_parent, sort_keys=True, indent=2)
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'script-src': [u"'none'"], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False, u'worker-src': [u"'none'"], u'media-src': [u'http:'], u'object-src': [u'http:']}]})
            res = False
            try:
                elt = self.marionette.find_element('id', 'test_result')
            except NoSuchElementException:
                res = True
            self.assertTrue(res, msg="http page sourcing http js")

            # https page sourcing http js
            self.marionette.navigate("%s/http_src.html" % self.https_url)
            csp_parent = get_csp()
            print "csp parent https page sourcing http js", json.dumps(csp_parent, sort_keys=True, indent=2)
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'media-src': [u'http:'], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False}]})
            res = False
            try:
                elt = self.marionette.find_element('id', 'test_result')
            except NoSuchElementException:
                res = True
            self.assertTrue(res, msg="https page sourcing http js")

            # https page sourcing http js (alternate hostname)
            self.marionette.navigate("%s/alternate_http_src.html" % self.https_url)
            csp_parent = get_csp()
            print "csp parent https page sourcing http js", json.dumps(csp_parent, sort_keys=True, indent=2)
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'media-src': [u'http:'], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False}]})
            res = False
            try:
                elt = self.marionette.find_element('id', 'test_result')
            except NoSuchElementException:
                res = True
            self.assertTrue(res, msg="https page sourcing http js (alternate hostname)")

            # http page sourcing https js
            self.marionette.navigate("%s/https_src.html" % self.http_url)
            csp_parent = get_csp()
            print "csp parent http page sourcing https js", json.dumps(csp_parent, sort_keys=True, indent=2)
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'script-src': [u"'none'"], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False, u'worker-src': [u"'none'"], u'media-src': [u'http:'], u'object-src': [u'http:']}]})
            res = False
            try:
                elt = self.marionette.find_element('id', 'test_result')
            except NoSuchElementException:
                res = True
            self.assertTrue(res, msg="http page sourcing https js")

            # https page sourcing https js
            self.marionette.navigate("%s/https_src.html" % self.https_url)
            csp_parent = get_csp()
            print "csp parent https page sourcing https js", json.dumps(csp_parent, sort_keys=True, indent=2)
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'media-src': [u'http:'], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False}]})
            res = True
            try:
                elt = self.marionette.find_element('id', 'test_result')
            except NoSuchElementException:
                res = False
            self.assertTrue(res, msg="https page sourcing https js")
            self.assertEqual('JavaScriptEnabled', elt.text, msg="https page sourcing https js")

            # https page sourcing https js (alternate hostname)
            self.marionette.navigate("%s/alternate_https_src.html" % self.https_url)
            csp_parent = get_csp()
            print "csp parent https page sourcing https js (alternate hostname)", json.dumps(csp_parent, sort_keys=True, indent=2)
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'media-src': [u'http:'], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False}]})
            res = True
            try:
                elt = self.marionette.find_element('id', 'test_result')
            except NoSuchElementException:
                res = False
            self.assertTrue(res, msg="https page sourcing https js (alternate hostname)")
            self.assertEqual('JavaScriptEnabled', elt.text,
                    msg="https page sourcing https js (alternate hostname)")

            # http page with http iframe
            self.marionette.navigate("%s/http_iframe.html" % self.http_url)
            csp_parent = get_csp()
            csp_iframe1 = get_iframe_csp_switch()
            csp_iframe2 = get_iframe_csp_direct()
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'media-src': [u'http:'], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False}]})
            print "csp parent http page with http iframe", json.dumps(csp_parent, sort_keys=True, indent=2)
            print "csp iframe1 http page with http iframe", json.dumps(csp_iframe1, sort_keys=True, indent=2)
            print "csp iframe2 http page with http iframe", json.dumps(csp_iframe2, sort_keys=True, indent=2)
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'script-src': [u"'none'"], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False, u'worker-src': [u"'none'"], u'media-src': [u'http:'], u'object-src': [u'http:']}]})
            iframe = self.marionette.find_element('id', 'iframe')
            self.marionette.switch_to_frame(iframe)
            res = False
            try:
                elt = self.marionette.find_element('id', 'test_result')
            except NoSuchElementException:
                res = True
            self.assertTrue(res, msg="http page with http iframe")
            self.marionette.switch_to_default_content()

            # http page with https iframe
            self.marionette.navigate("%s/https_iframe.html" % self.http_url)
            csp_parent = get_csp()
            csp_iframe1 = get_iframe_csp_switch()
            csp_iframe2 = get_iframe_csp_direct()
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'media-src': [u'http:'], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False}]})
            print "csp parent http page with https iframe", json.dumps(csp_parent, sort_keys=True, indent=2)
            print "csp iframe1 http page with https iframe", json.dumps(csp_iframe1, sort_keys=True, indent=2)
            print "csp iframe2 http page with https iframe", json.dumps(csp_iframe2, sort_keys=True, indent=2)
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'script-src': [u"'none'"], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False, u'worker-src': [u"'none'"], u'media-src': [u'http:'], u'object-src': [u'http:']}]})
            iframe = self.marionette.find_element('id', 'iframe')
            self.marionette.switch_to_frame(iframe)
            res = False
            try:
                elt = self.marionette.find_element('id', 'test_result')
            except NoSuchElementException:
                res = True
            self.assertTrue(res, msg="http page with https iframe")
            self.marionette.switch_to_default_content()

            # https page with http iframe
            self.marionette.navigate("%s/http_iframe.html" % self.https_url)
            csp_parent = get_csp()
            csp_iframe1 = get_iframe_csp_switch()
            csp_iframe2 = get_iframe_csp_direct()
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'media-src': [u'http:'], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False}]})
            print "csp parent https page with http iframe", json.dumps(csp_parent, sort_keys=True, indent=2)
            print "csp iframe1 https page with http iframe", json.dumps(csp_iframe1, sort_keys=True, indent=2)
            print "csp iframe2 https page with http iframe", json.dumps(csp_iframe2, sort_keys=True, indent=2)
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'media-src': [u'http:'], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False}]})
            iframe = self.marionette.find_element('id', 'iframe')
            self.marionette.switch_to_frame(iframe)
            res = False
            try:
                elt = self.marionette.find_element('id', 'test_result')
            except NoSuchElementException:
                res = True
            self.assertTrue(res, msg="https page with http iframe")
            self.marionette.switch_to_default_content()

            # https page sourcing https js (alternate hostname)
            self.marionette.navigate("%s/alternate_http_iframe.html" % self.https_url)
            csp_parent = get_csp()
            csp_iframe1 = get_iframe_csp_switch()
            csp_iframe2 = get_iframe_csp_direct()
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'media-src': [u'http:'], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False}]})
            print "csp parent https page sourcing https js (alternate hostname)", json.dumps(csp_parent, sort_keys=True, indent=2)
            print "csp iframe1 https page sourcing https js (alternate hostname)", json.dumps(csp_iframe1, sort_keys=True, indent=2)
            print "csp iframe2 https page sourcing https js (alternate hostname)", json.dumps(csp_iframe2, sort_keys=True, indent=2)
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'media-src': [u'http:'], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False}]})
            iframe = self.marionette.find_element('id', 'iframe')
            self.marionette.switch_to_frame(iframe)
            res = False
            try:
                elt = self.marionette.find_element('id', 'test_result')
            except NoSuchElementException:
                res = True
            self.assertTrue(res, msg="https page sourcing https js (alternate hostname)")
            self.marionette.switch_to_default_content()

            # https page with https iframe
            self.marionette.navigate("%s/https_iframe.html" % self.https_url)
            csp_parent = get_csp()
            csp_iframe1 = get_iframe_csp_switch()
            csp_iframe2 = get_iframe_csp_direct()
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'media-src': [u'http:'], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False}]})
            print "csp parent https page with https iframe", json.dumps(csp_parent, sort_keys=True, indent=2)
            print "csp iframe1 https page with https iframe", json.dumps(csp_iframe1, sort_keys=True, indent=2)
            print "csp iframe2 https page with https iframe", json.dumps(csp_iframe2, sort_keys=True, indent=2)

            iframe = self.marionette.find_element('id', 'iframe')
            self.marionette.switch_to_frame(iframe)
            res = True
            try:
                elt = self.marionette.find_element('id', 'test_result')
            except NoSuchElementException:
                res = False
            self.assertTrue(res, msg="https page with https iframe")
            self.assertEqual(elt.text, 'JavaScriptEnabled',
                    msg="https page with https iframe")
            self.marionette.switch_to_default_content()

            # https page with https iframe (alternate hostname)
            self.marionette.navigate("%s/alternate_https_iframe.html" % self.https_url)
            csp_parent = get_csp()
            csp_iframe1 = get_iframe_csp_switch()
            csp_iframe2 = get_iframe_csp_direct()
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'media-src': [u'http:'], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False}]})
            print "csp parent https page with https iframe (alternate hostname)", json.dumps(csp_parent, sort_keys=True, indent=2)
            print "csp iframe1 https page with https iframe (alternate hostname)", json.dumps(csp_iframe1, sort_keys=True, indent=2)
            print "csp iframe2 https page with https iframe (alternate hostname)", json.dumps(csp_iframe2, sort_keys=True, indent=2)
            # self.assertDictEqual(get_csp(), {u'csp-policies': [{u'media-src': [u'http:'], u'report-uri': [u'https://noscript-csp.invalid/__NoScript_Probe__/'], u'report-only': False}]})
            iframe = self.marionette.find_element('id', 'iframe')
            self.marionette.switch_to_frame(iframe)
            res = True
            try:
                elt = self.marionette.find_element('id', 'test_result')
            except NoSuchElementException:
                res = False
            self.assertTrue(res, msg="https page with https iframe")
            self.assertEqual(elt.text, 'JavaScriptEnabled',
                    msg="https page with https iframe")
            self.marionette.switch_to_default_content()

