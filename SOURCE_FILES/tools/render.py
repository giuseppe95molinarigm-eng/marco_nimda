import sys, weasyprint, time
t=time.time()
doc = weasyprint.HTML(sys.argv[1]).render()
print('pages', len(doc.pages), 'secs', round(time.time()-t,1))
doc.write_pdf(sys.argv[2])
