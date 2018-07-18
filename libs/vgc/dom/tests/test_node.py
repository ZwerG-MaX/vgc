#!/usr/bin/python3

# Copyright 2018 The VGC Developers
# See the COPYRIGHT file at the top-level directory of this distribution
# and at https://github.com/vgc/vgc/blob/master/COPYRIGHT
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

import unittest

from vgc.dom import Document, Element, Node, NodeType

def getChildNames(node):
    return [child.name for child in node.children]

class TestNodeType(unittest.TestCase):

    def testValues(self):
        NodeType.Document
        NodeType.Element

class TestNode(unittest.TestCase):

    def testConstructor(self):
        with self.assertRaises(TypeError):
            node = Node()

    def testNodeType(self):
        doc = Document()
        element = Element(doc, "foo")
        self.assertEqual(doc.nodeType, NodeType.Document)
        self.assertEqual(element.nodeType, NodeType.Element)

    def testParentChildRelationships(self):
        doc = Document()
        n1 = Element(doc, "foo")

        self.assertEqual(n1.parent,          doc)
        self.assertEqual(n1.firstChild,      None)
        self.assertEqual(n1.lastChild,       None)
        self.assertEqual(n1.previousSibling, None)
        self.assertEqual(n1.nextSibling,     None)

        n2 = Element(n1, "bar")
        n3 = Element(n1, "bar")
        n4 = Element(n1, "bar")

        self.assertEqual(n1.parent,          doc)
        self.assertEqual(n1.firstChild,      n2)
        self.assertEqual(n1.lastChild,       n4)
        self.assertEqual(n1.previousSibling, None)
        self.assertEqual(n1.nextSibling,     None)

        self.assertEqual(n2.parent,          n1)
        self.assertEqual(n2.firstChild,      None)
        self.assertEqual(n2.lastChild,       None)
        self.assertEqual(n2.previousSibling, None)
        self.assertEqual(n2.nextSibling,     n3)

        self.assertEqual(n3.parent,          n1)
        self.assertEqual(n3.firstChild,      None)
        self.assertEqual(n3.lastChild,       None)
        self.assertEqual(n3.previousSibling, n2)
        self.assertEqual(n3.nextSibling,     n4)

        self.assertEqual(n4.parent,          n1)
        self.assertEqual(n4.firstChild,      None)
        self.assertEqual(n4.lastChild,       None)
        self.assertEqual(n4.previousSibling, n3)
        self.assertEqual(n4.nextSibling,     None)

    def testChildren(self):
        doc = Document()
        n1 = Element(doc, "foo")
        n2 = Element(n1, "bar1")
        n3 = Element(n1, "bar2")
        n4 = Element(n1, "bar3")
        self.assertEqual(getChildNames(n1), ["bar1", "bar2", "bar3"])

    def testDocument(self):
        doc = Document()
        self.assertEqual(doc.document, doc)

        n1 = Element(doc, "foo")
        n2 = Element(n1, "bar")
        self.assertEqual(n1.document, doc)
        self.assertEqual(n2.document, doc)

    # TODO Add tests for thrown exceptions when trying invalid operations

    def testAppendChild(self):
        doc = Document()
        n1 = Element(doc, "n1")
        n2 = Element(n1, "n2")
        n3 = Element(n2, "n3")
        self.assertEqual(getChildNames(doc), ["n1"])
        self.assertEqual(getChildNames(n1),  ["n2"])
        self.assertEqual(getChildNames(n2),  ["n3"])
        self.assertEqual(getChildNames(n3),  [])
        n1.appendChild(n3)
        self.assertEqual(getChildNames(doc), ["n1"])
        self.assertEqual(getChildNames(n1),  ["n2", "n3"])
        self.assertEqual(getChildNames(n2),  [])
        self.assertEqual(getChildNames(n3),  [])

    def testAppendChildDocument(self):
        doc1 = Document()
        n1 = Element(doc1, "foo")
        doc2 = Document()
        self.assertFalse(doc1.canAppendChild(doc2))
        self.assertFalse(n1.canAppendChild(doc1))
        self.assertFalse(n1.canAppendChild(doc2))

    def testAppendChildRootElement(self):
        doc = Document()
        n1 = Element(doc, "foo")
        n2 = Element(n1, "bar")
        self.assertEqual(doc.rootElement, n1)
        self.assertFalse(doc.canAppendChild(n2))

    def testRemoveChild(self):
        doc = Document()
        root = Element(doc, "root")
        n1 = Element(root, "n1")
        n2 = Element(root, "n2")
        n3 = Element(root, "n3")
        n4 = Element(root, "n4")
        self.assertEqual(getChildNames(root), ["n1", "n2", "n3", "n4"])

        root.removeChild(n3)
        self.assertEqual(getChildNames(root), ["n1", "n2", "n4"])

        root.removeChild(n4)
        self.assertEqual(getChildNames(root), ["n1", "n2"])

        root.removeChild(n1)
        self.assertEqual(getChildNames(root), ["n2"])

        root.removeChild(n2)
        self.assertEqual(getChildNames(root), [])

if __name__ == '__main__':
    unittest.main()
