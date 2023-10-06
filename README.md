# LeDA: A System for Legal Data Annotation
LeDA is basically a tool that can be used to annotate documents (e.g., Legal, News articles, etc.). Moreover, LeDA provides advanced features such as **Inter-Annotator Agreement** (to measure the similarity between two annotators for the same document) computation, **Adjudication** (to mitigate the low IAA score issue), and **Dynamic Tag** (annotator can enrich the tag-list during annotation). In order to, explore the features of LeDA, we have considered legal documents.<br />
In this study, we delve into Supreme Court documents from the Indian judiciary, with a particular emphasis on case documents related to criminal activities as defined by the **Indian Penal Code (IPC) sections**. The IPC encompasses a total of 511 sections distributed across 23 chapters, and our specific focus centers on Chapter XVI.
# 1. Why did we choose murder-oriented documents?
As we mentioned in this paper, we considered IPC 302 (Punishment for Murder) and some similar IPCs such as IPC 299, IPC 300, and IPC 307, and most importantly highest number of cases are related to murder, as shown in the following figure. In particular, we have considered section 299 to section 311 of IPC which is basically "of offenses affecting the human body" and we have discussed all of them briefly in Section 2.  <br/>
![ipc_3](https://github.com/subinayadhikary/LeDA/assets/50978159/e1f6674a-938a-4060-b0e6-a98054251c67)
# 2. Indian Penal Code (IPC) section details
- *299.* **Culpable homicide.** <br />
- *300.* **Murder.** **When culpable homicide is not murder.** <br />
- *301.* **Culpable homicide by causing death of person other than person whose death was intended.** <br />
- *302.* **Punishment for murder.** <br />
- *303.* **Punishment for murder by life-convict.** <br />
- *304.* **Punishment for culpable homicide not amounting to murder.** <br />
- *304A.* **Causing death by negligence.** <br />
- *304B.* **Dowry death.** <br />
- *305.* **Abetment of suicide of child or insane person.** <br />
- *306.* **Abetment of suicide.** <br />
- *307.* **Attempt to murder. Attempts by life-convicts.** <br />
- *308.* **Attempt to commit culpable homicide.** <br />
- *309.* **Attempt to commit suicide.** <br />
- *310.* **Thug**- Whoever, at any time after the passing of this Act, shall have been habitually associated
with any other or others for the purpose of committing robbery or child-stealing by means of or
accompanied with murder, is a thug. <br />
- *311.* **Punishment**- Whoever is a thug, shall be punished with 4 [imprisonment for life], and shall also
be liable to fine. <br />
For getting more details about the Indian Penal Code, you may visit https://legislative.gov.in/sites/default/files/A1860-45.pdf.  <br />
# 3. Interface of LeDA
![img_3](https://github.com/subinayadhikary/LeDA/assets/50978159/bc06a779-6665-4221-bbfb-e803583039e2)
Here we have mentioned all the features of LeDA by highlighting them. <br />
'A': **is used to upload documents**; 'B': **selects a document from a list**; 'C': **indicates that the document is annotated by both the annotators**; 'D': **indicates the IAA score**; 'E': **computes the IAA score**; 'F': **button to delete a document**; 'G': **button to add new a tag**; 'H': **selected document**; 'I': **set of tags**; 'J': **search documents tag-wise**; 'K': **buttons to add, remove or save the highlighted span and labels**; 'L': **highlighted span**; 'M': **label for highlighted span**; 'N': **search a document**.

# 4. The LeDA demo
The preview of our tool is available at https://tinyurl.com/annotationtool.


