#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import xml.etree.ElementTree as ET

destTree = ET.parse('qt_zh_CN.ts')
destRoot = destTree.getroot()
srcTree = ET.parse('qtbase_ja.ts')
srcRoot = srcTree.getroot()

for srcContext in srcRoot.findall('context'):
    hasThisContext = False
    srcName = srcContext.find('name').text
    for destContext in destRoot.findall('context'):
        destName = destContext.find('name').text
        if srcName == destName:
            hasThisContext = True
            for srcMessage in srcContext.findall('message'):
                hasThisMessage = False
                srcSource = srcMessage.find('source').text
                for destMessage in destContext.findall('message'):
                    destSource = destMessage.find('source').text
                    if srcSource == destSource:
                        hasThisMessage = True
                        pass
                if not hasThisMessage:
                    if not srcRoot.attrib['language'].startswith('zh'):
                        srcTranslation = srcMessage.find('translation')
                        srcTranslation.text = ''
                        srcTranslation.set('type', 'unfinished')
                    destContext.append(srcMessage)
    if not hasThisContext:
        if not srcRoot.attrib['language'].startswith('zh'):
            for srcTranslation in srcContext.iter('translation'):
                srcTranslation.text = ''
                srcTranslation.set('type', 'unfinished')
        destRoot.append(srcContext)

for destMessage in destRoot.iter('message'):
    for destLocation in destMessage.findall('location'):
        destMessage.remove(destLocation)

destTree.write('qt_zh_CN.ts', encoding='utf-8')
