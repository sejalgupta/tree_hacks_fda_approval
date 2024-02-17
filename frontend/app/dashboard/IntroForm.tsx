import React from "react";

function IntroForm(props: { onSubmit: (e: React.FormEvent<HTMLFormElement>) => void;}) {
    return (
        <section id="intro-form">
            <h1 className="text-center">Enter details of your device</h1>
            <form onSubmit={props.onSubmit}>
                <div className="form-group my-5">
                    <label htmlFor="device-description" className="block text-sm font-medium mb-2 dark:text-white">
                        Device Description
                    </label>
                    <textarea id="device-description" className="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600" rows={3} placeholder="Say hi, we'll be happy to chat with you." aria-describedby="hs-textarea-helper-text">
                    </textarea>
                    <p className="text-xs text-gray-500 mt-2" id="hs-textarea-helper-text">
                        We'll get back to you soon.
                    </p>
                </div>
                <div className="form-group my-5">
                    <label htmlFor="use-indication" className="block text-sm font-medium mb-2 dark:text-white">
                        Indication of use
                    </label>
                    <textarea id="use-indication" className="py-3 px-4 block w-full border-gray-200 rounded-lg text-sm focus:border-blue-500 focus:ring-blue-500 disabled:opacity-50 disabled:pointer-events-none dark:bg-slate-900 dark:border-gray-700 dark:text-gray-400 dark:focus:ring-gray-600" rows={3} placeholder="Say hi, we'll be happy to chat with you." aria-describedby="hs-textarea-helper-text">
                    </textarea>
                    <p className="text-xs text-gray-500 mt-2" id="hs-textarea-helper-text">
                        We'll get back to you soon.
                    </p>
                </div>
                <div className="form-group my-5 text-center">
                    <button type="submit" className="py-3 px-4 inline-flex items-center gap-x-2 text-sm font-semibold rounded-lg border border-transparent bg-blue-600 text-white hover:bg-blue-700 disabled:opacity-50 disabled:pointer-events-none dark:focus:outline-none dark:focus:ring-1 dark:focus:ring-gray-600">
                        Submit
                    </button>
                </div>
            </form>
        </section>
    );
}

export default IntroForm;