def prompts(companyA = "", companyB = "", employeeName = "", employeePosition = "", custom =""):
    
    if companyA != "" and companyB != "":
        nameString = f"The name of the aquiring company is {companyA} and the name of the target company is {companyB}."
    else: 
        nameString = ""
        
    custom = f"""Create a fictitious {custom} for {companyA}"""

    hostileTakeover = f"""Create a fictitious document regarding a hostile takeover. 
    Make this document as realistic as possible and lengthy. 
    {nameString}
    The format should be in markdown with the relevant headings, lists, bold text and italics"""

    annualReport = f"""Create a Corporate Annual Report for the company {companyA} that include financial statements, market trends, and future growth plans. 
    Use these reports to provide players with an overview of the company's performance, strengths, and weaknesses."""

    investmentProspects = f"""Create an Investment Prospectuses Document for new investment opportunities, such as initial public offerings (IPOs) or venture capital investments. 
    The documents should provide information about the investment opportunity, including the company's ({companyA}) business model, financial performance, and growth potential."""

    mergersAqui= f"""Create a proposal for mergers and acquisitions between the company {companyA} and another company {companyB}. 
    Use the proposals to provide information about the companies involved, the potential benefits of the merger or acquisition, and the proposed terms of the deal."""

    loanDoc = f"""Create a loan agreement document between financial institutions and the company {companyA}. 
    Use these agreements to provide information about the terms of the loan, including interest rates, repayment schedules, and collateral requirements."""

    regFilling = f""" Create a Regulatory Filings Document for the company {companyA},
    such as SEC filings or annual reports to regulatory bodies. 
    The Document should provide information about the legal and regulatory environment in which the companies operate. """

    creditRating = f"""Create credit rating reports for the company {companyA} 
    that include information on its creditworthiness and likelihood of defaulting on loans. 
    Use these reports to provide players with information about the risks associated with investing in the company."""

    financialStatement = f"""Create financial statements for the company {companyA} 
    that include balance sheets, income statements, and cash flow statements. 
    Use these statements to provide a snapshot of the company's financial health. """

    shareholderReport = f""" Create shareholder reports for the company {companyA} 
    that include information on dividend payouts, share prices, and voting rights. 
    Use the report to give a sense of the company's relationship with its investors. """

    employeeReview = f""" Create employee performance reviews for key personnel at the company {companyA}, including senior executives and managers. 
    Use these reviews to provide insights into the leadership and management of the company. """

    if employeeName != "" or employeePosition != "":
        employeeReview = f""" Create an employee performance reviews for key personnel at the company {companyA}, 
    for {employeeName} at position {employeePosition}.  
    Use this review to provide insights into the companies relationship with the employee {employeeName}. """

    esgReport = f"""Create an ESG (Environmental, Social and Governance) report for the company {companyA} 
    that includes information on its sustainability practices, social impact, and governance structure.
    Use this report to provide information about the company's ethical and social responsibility. """

    litigationDocument = f""" Create a document related to legal cases involving the company {companyA}, 
    including court filings, settlement agreements, and legal opinions. 
    Use these documents to provide information about the legal risks associated with investing in the company. """

    marketResearch = f""" Create marketing research reports for the company {companyA} 
    that include information on consumer trends, market opportunities, and the competitive landscape. 
    Use these reports to provide players with insights into the market forces shaping the company's strategies and growth prospects. """
    
    prompts = {"custom": custom, "hostileTakeover": hostileTakeover, "annualReport": annualReport, "investmentProspects": investmentProspects, "mergersAqui": mergersAqui, "loanDoc": loanDoc, "regFilling": regFilling, "creditRating": creditRating, "financialStatement": financialStatement, "shareholderReport": shareholderReport, "employeeReview": employeeReview, "esgReport": esgReport, "litigationDocument": litigationDocument, "marketResearch": marketResearch}
    
    return prompts