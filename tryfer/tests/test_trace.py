# Copyright 2012 Rackspace Hosting, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import math

import mock

from zope.interface.verify import verifyObject

from unittest import TestCase

from tryfer.interfaces import ITrace, IAnnotation, IEndpoint
from tryfer.trace import Trace, Annotation, Endpoint

MAX_ID = math.pow(2, 63) - 1


class TraceTests(TestCase):

    def test_new_Trace(self):
        t = Trace('test_trace')
        self.assertNotEqual(t.trace_id, None)
        self.assertIsInstance(t.trace_id, (int, long))
        self.failIf(t.trace_id >= MAX_ID)

        self.assertNotEqual(t.span_id, None)
        self.assertIsInstance(t.span_id, (int, long))
        self.failIf(t.span_id >= MAX_ID)

        self.assertEqual(t.parent_span_id, None)

    def test_Trace_child(self):
        t = Trace('test_trace', trace_id=1, span_id=1)

        c = t.child('child_test_trace')

        self.assertEqual(c.trace_id, 1)
        self.assertEqual(c.parent_span_id, 1)
        self.assertNotEqual(c.span_id, 1)

    def test_record_invokes_tracer(self):
        tracer = mock.Mock()

        t = Trace('test_trace', trace_id=1, span_id=1, tracers=[tracer])
        annotation = Annotation.client_send(timestamp=0)
        t.record(annotation)

        tracer.record.assert_called_with([(t, (annotation,))])

    def test_record_sets_annotation_endpoint(self):
        tracer = mock.Mock()
        web_endpoint = Endpoint('127.0.0.1', 8080, 'web')

        t = Trace('test_trace', trace_id=1, span_id=1, tracers=[tracer])
        t.set_endpoint(web_endpoint)
        annotation = Annotation.client_send(timestamp=1)
        t.record(annotation)

        tracer.record.assert_called_with([(t, (annotation,))])

        self.assertEqual(annotation.endpoint, web_endpoint)

    def test_equality(self):
        self.assertEqual(
            Trace('test_trace', trace_id=1, span_id=1, parent_span_id=1),
            Trace('test_trace2', trace_id=1, span_id=1, parent_span_id=1))

    def test_inequality(self):
        trace = Trace('test_trace', trace_id=1, span_id=1, parent_span_id=1)

        self.assertNotEqual(trace, None)

        self.assertNotEqual(
            trace,
            Trace('test_trace', trace_id=2, span_id=1, parent_span_id=1))
        self.assertNotEqual(
            trace,
            Trace('test_trace', trace_id=1, span_id=2, parent_span_id=1))
        self.assertNotEqual(
            trace,
            Trace('test_trace', trace_id=1, span_id=1, parent_span_id=2))


class AnnotationTests(TestCase):
    def setUp(self):
        self.time_patcher = mock.patch('tryfer.trace.time.time')
        self.time = self.time_patcher.start()
        self.time.return_value = 1

    def tearDown(self):
        self.time_patcher.stop()

    def test_timestamp(self):
        a = Annotation.timestamp('test')
        self.assertEqual(a.value, 1000000)
        self.assertEqual(a.name, 'test')
        self.assertEqual(a.annotation_type, 'timestamp')

    def test_client_send(self):
        a = Annotation.client_send()
        self.assertEqual(a.value, 1000000)
        self.assertEqual(a.name, 'cs')
        self.assertEqual(a.annotation_type, 'timestamp')

    def test_client_recv(self):
        a = Annotation.client_recv()
        self.assertEqual(a.value, 1000000)
        self.assertEqual(a.name, 'cr')
        self.assertEqual(a.annotation_type, 'timestamp')

    def test_server_send(self):
        a = Annotation.server_send()
        self.assertEqual(a.value, 1000000)
        self.assertEqual(a.name, 'ss')
        self.assertEqual(a.annotation_type, 'timestamp')

    def test_server_recv(self):
        a = Annotation.server_recv()
        self.assertEqual(a.value, 1000000)
        self.assertEqual(a.name, 'sr')
        self.assertEqual(a.annotation_type, 'timestamp')

    def test_equality(self):
        self.assertEqual(
            Annotation('foo', 'bar', 'string'),
            Annotation('foo', 'bar', 'string'))

        self.assertEqual(
            Annotation('foo', 'bar', 'string',
                       Endpoint('127.0.0.1', 0, 'test')),
            Annotation('foo', 'bar', 'string',
                       Endpoint('127.0.0.1', 0, 'test')))

    def test_inequality(self):
        annotation = Annotation('foo', 'bar', 'string')

        self.assertNotEqual(annotation, None)

        self.assertNotEqual(
            annotation,
            Annotation('foo1', 'bar', 'string'))
        self.assertNotEqual(
            annotation,
            Annotation('foo', 'bar1', 'string'))
        self.assertNotEqual(
            annotation,
            Annotation('foo', 'bar', 'string1'))
        self.assertNotEqual(
            annotation,
            Annotation('foo', 'bar', 'string',
                       Endpoint('127.0.0.1', 0, 'test')))
        self.assertNotEqual(
            Annotation('foo', 'bar', 'string',
                       Endpoint('127.0.0.1', 0, 'test2')),
            Annotation('foo', 'bar', 'string',
                       Endpoint('127.0.0.1', 0, 'test')))


class EndpointTests(TestCase):
    def test_equality(self):
        self.assertEqual(
            Endpoint('127.0.0.1', 0, 'test'),
            Endpoint('127.0.0.1', 0, 'test'))

    def test_inequality(self):
        endpoint = Endpoint('127.0.0.1', 0, 'test')

        self.assertNotEqual(endpoint, None)

        self.assertNotEqual(
            endpoint,
            Endpoint('127.0.0.2', 0, 'test'))
        self.assertNotEqual(
            endpoint,
            Endpoint('127.0.0.1', 1, 'test'))
        self.assertNotEqual(
            endpoint,
            Endpoint('127.0.0.1', 0, 'test2'))

