"""
\draw_res_axis_label = ["(p_{T}^{GEN} - p_{T}^{L1}) / p_{T}^{GEN}", "(p_{T,GEN}^{-1} - p_{T,L1}^{-1}) / p_{T,GEN}^{-1}"]
draw_res_option = ["(GEN_pt - pow(2, BDTG_AWB_Sq))/GEN_pt", "(((1./GEN_pt) - (1./pow(2, BDTG_AWB_Sq)))/(1./GEN_pt))"]
draw_res_label = ["diffOverGen", "invDiffOverInvGen"]
res_type = ["mu", "sigma"]



if options.resolutions:

  if options.res1D:

    for k in range(len(draw_res_option)):

      for l in range(len(pt_cut)):

	resolutions = []

	for ee in range(0,2):
	  res = draw_res(evt_trees[ee], 64, -10, 10, draw_res_option[k] , bdt_pt(pt_cut[l]) )
	  resolutions.append(res)

	c1 = TCanvas("c1")
	draw_multiple(resolutions, " ; "+draw_res_axis_label[k]+" ; ", drawOptions1D, lineColors, legendEntries, pt_cut[l])
	makePlots(c1, plotDir,  "ptres1D_"+draw_res_label[k]+"_pt"+str(pt_str[l]) )
	c1.Close()


  if options.res1DvsPt and options.single_pt: print "Error: Must set single_pt to false in order to plot resolutions vs Pt."
  if options.res1DvsPt and not options.single_pt:

    mu_res = np.empty((len(evt_trees),len(pt_cut)))
    mu_res_err = np.empty((len(evt_trees),len(pt_cut)))
    sigma_res = np.empty((len(evt_trees),len(pt_cut)))
    sigma_res_err = np.empty((len(evt_trees),len(pt_cut)))
    xErrors = np.zeros((len(evt_trees),len(pt_cut)))

    for k in range(len(draw_res_option)):

      for l in range(len(pt_cut)):

	for ee in range(0,2):
	  res = draw_res(evt_trees[ee], 64, -10, 10, draw_res_option[k], bdt_pt(pt_cut[l]) )

	  mu_res[ee][l] = res.GetMean()
	  mu_res_err[ee][l] = res.GetMeanError()
	  sigma_res[ee][l] = res.GetRMS()
	  sigma_res_err[ee][l] = res.GetRMSError()

      draw_multi_resVsPt(len(evt_trees), mu_res, mu_res_err, xErrors, 'p_{T}^{GEN} (GeV)', '#mu '+draw_res_axis_label[k], lineColors, pt_cut, legendEntries, draw_res_label[k], res_type[0])
      draw_multi_resVsPt(len(evt_trees), sigma_res, sigma_res_err, xErrors, 'p_{T}^{GEN} (GeV)', '#sigma '+draw_res_axis_label[k], lineColors, pt_cut, legendEntries, draw_res_label[k], res_type[1])



  if options.res1DvsEta:

    for k in range(len(draw_res_option)):

      #Define the eta range from the negative+positive endcap in a single array.
      eta_range = []
      nbins = int(round(abs((float(eta_min[0]) -  float(eta_max[0]) ) / 0.1)))

      for i in range(nbins+1):
	eta_range.append(round(-1*float(eta_max[0]) + 0.1*i,1))
      for i in range(nbins+1):
	eta_range.append(round(float(eta_min[0]) + 0.1*i,1))

      #2x2 arrays to hold the mean and width (and errors) of the pt resolutions.
      mu_res = np.zeros((len(evt_trees),len(eta_range)-2))
      mu_res_err = np.zeros((len(evt_trees),len(eta_range)-2))
      sigma_res = np.zeros((len(evt_trees),len(eta_range)-2))
      sigma_res_err = np.zeros((len(evt_trees),len(eta_range)-2))
      xErrors = np.zeros((len(evt_trees),len(eta_range)-2))

      for l in range(len(pt_cut)):

	for i in range(len(eta_range)-2):

	  for ee in range(0,len(trainings)):
	    #Add a check to skip the bin at the boundary between endcaps (-1.2 to 1.2).
	    if i<len(eta_range)/2 - 1: res = draw_resVsEta(evt_trees[ee], 64, -10, 10, draw_res_option[k], bdt_pt(pt_cut[l]), gen_pt_cut(pt_cut[l]), gen_eta_cut(eta_range[i], eta_range[i+1]) )
	    if i>=len(eta_range)/2 - 1: res = draw_resVsEta(evt_trees[ee], 64, -10, 10, draw_res_option[k], bdt_pt(pt_cut[l]), gen_pt_cut(pt_cut[l]), gen_eta_cut(eta_range[i+1], eta_range[i+2]) )

	    mu_res[ee][i] = res.GetMean()
	    mu_res_err[ee][i] = res.GetMeanError()
	    sigma_res[ee][i] = res.GetRMS()
	    sigma_res_err[ee][i] = res.GetRMSError()

      #Remove the bins at the endcaps boundries that won't be plotted.
      eta_range.remove(-1*eta_min[0])
      eta_range.remove(eta_min[0])

      draw_multi_resVsEta(len(evt_trees), mu_res, mu_res_err, xErrors, '#eta^{GEN}', '#mu '+draw_res_axis_label[k], lineColors, eta_range, legendEntries, draw_res_label[k], res_type[0])
      draw_multi_resVsEta(len(evt_trees), sigma_res, sigma_res_err, xErrors, '#eta^{GEN}', '#sigma '+draw_res_axis_label[k], lineColors, eta_range, legendEntries, draw_res_label[k], res_type[1])



  if options.res2D:

    for ee in range(0,len(trainings)):

      draw_res2D(evt_trees[ee], 100, 0, 5.7, 100, 0, 5.5, "BDTG_AWB_Sq:log2(GEN_pt)", legendEntries[ee], outFileString[ee])
"""
